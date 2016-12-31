from __future__ import unicode_literals

from django.dispatch import receiver

from base.signals import update_projection
from base.models import EventMixin, ProjectionMixin
from products import events
from products.reducers import Reducer


class ProductEvent(EventMixin):

    reducer = Reducer()

    # base events
    create_event = events.CreateEvent()
    update_event = events.UpdateEvent()
    delete_event = events.DeleteEvent()
    attr_delete_event = events.AttributeDeleteEvent()

    # custom events
    add_category_event = events.AddCategoryEvent()
    remove_category_event = events.RemoveCategoryEvent()

    @classmethod
    def get_projection(cls):
        return ProductProjection


@receiver(update_projection, sender=ProductEvent)
def project(sender, event, *args, **kwargs):
    projection = sender.get_projection()
    projection.project(event.entity_id)


class ProductProjection(ProjectionMixin):

    event_model = ProductEvent
