from django.db import models
from base.exceptions import EntityNotCreated


class EventLogManager(models.Manager):

    def created_events(self):
        return self.get_queryset().filter(
            event_type='Created'
        )

    def updated_events(self):
        return self.get_queryset().filter(
            event_type='Updated'
        )

    def deleted_events(self):
        return self.get_queryset().filter(
            event_type='Deleted'
        )

    def get_last_checkpoint(self, entity_id):
        last_event = self.get_queryset().filter(
            entity_id=entity_id
        ).latest('checkpoint')
        if last_event:
            return last_event.checkpoint
        raise EntityNotCreated(
            "%s.entity_id == %s, does not exist " % (
                self.model, entity_id
            )
        )

    def exists(self, entity_id):
        return self.get_queryset().filter(
            entity_id=entity_id,
            event_type=self.model.delete_event.EVENT_TYPE_NAME
        ).count() < 1

    def get_current_state(self, entity_id):
        events = self.get_queryset().filter(
            entity_id=entity_id
        ).order_by('checkpoint')
        return reduce(self.model.reducer, events, {})

    def get_current_state_from_projection(self, entity_id):
        projection_model = self.model.get_projection()
        try:
            projection = projection_model.objects.get(entity_id=entity_id)
            # All events after the snapshot
            events = self.get_queryset().filter(
                entity_id=entity_id,
                checkpoint__gt=projection.checkpoint
            ).order_by('checkpoint')
            return reduce(self.model.reducer, events, projection.view)
        except projection_model.DoesNotExist:
            return self.get_current_state(entity_id)
