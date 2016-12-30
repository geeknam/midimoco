from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from base.managers import EventLogManager


class EventMixin(models.Model):

    entity_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    checkpoint = models.IntegerField(db_index=True)
    event_type = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()

    events_manager = EventLogManager()

    class Meta:
        abstract = True
        unique_together = ('entity_id', 'checkpoint')

    def __unicode__(self):
        return '{entity_name}:{entity_id}:{event_type}'.format(
            entity_name=self.__class__.__name__,
            entity_id=self.entity_id,
            event_type=self.event_type
        )

    @classmethod
    def get_projection(cls):
        raise NotImplementedError

    @classmethod
    def reducer(cls, aggregate, next_event):
        state = dict(aggregate)
        if next_event.event_type == cls.create_event.EVENT_TYPE_NAME:
            return next_event.data
        if next_event.event_type == cls.update_event.EVENT_TYPE_NAME:
            state.update(next_event.data)
            return state
        if next_event.event_type == cls.attr_delete_event.EVENT_TYPE_NAME:
            for attr in next_event.data.get('attributes', []):
                state.pop(attr, None)
            return aggregate
        if next_event.event_type == cls.delete_event.EVENT_TYPE_NAME:
            raise cls.DoesNotExist(
                'Entity deleted on %s' % next_event.created_at)
        return state


class ProjectionMixin(models.Model):

    entity_id = models.UUIDField(primary_key=True, default=None)
    checkpoint = models.IntegerField(db_index=True)
    view = JSONField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return '{entity_name}:{entity_id}:{checkpoint}'.format(
            entity_name=self.__class__.__name__,
            entity_id=self.entity_id,
            checkpoint=self.checkpoint
        )

    @classmethod
    def project(cls, entity_id):
        manager = cls.event_model.events_manager
        current_state = manager.get_current_state(entity_id)
        checkpoint = manager.get_last_checkpoint(entity_id)
        obj, created = cls.objects.update_or_create(
            entity_id=entity_id,
            defaults={
                'checkpoint': checkpoint,
                'view': current_state
            }
        )
        return obj
