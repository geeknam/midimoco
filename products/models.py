from __future__ import unicode_literals

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


class ProductProjection(ProjectionMixin):

    event_model = ProductEvent
