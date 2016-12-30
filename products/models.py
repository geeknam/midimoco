from __future__ import unicode_literals

from base.models import EventMixin, ProjectionMixin
from products import events


class ProductEvent(EventMixin):

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

    @classmethod
    def reducer(cls, aggregate, next_event):
        state = super(ProductEvent, cls).reducer(aggregate, next_event)
        if next_event.event_type == cls.add_category_event.EVENT_TYPE_NAME:
            state.setdefault(
                cls.add_category_event.relation_key, []
            ).append(next_event.data)
            return state
        if next_event.event_type == cls.remove_category_event.EVENT_TYPE_NAME:
            state.get(
                cls.remove_category_event.relation_key, []
            ).remove(next_event.data)
            return state
        return state


class ProductProjection(ProjectionMixin):

    event_model = ProductEvent
