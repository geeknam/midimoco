from base import events
from products import forms


class CreateEvent(events.BaseCreateEvent):

    form_class = forms.ProductForm


class UpdateEvent(events.BaseUpdateEvent):

    form_class = forms.ProductUpdateForm


class DeleteEvent(events.BaseDeleteEvent):

    form_class = forms.ProductDeleteForm


class AttributeDeleteEvent(events.BaseAttributeDeleteEvent):

    form_class = forms.ProductAttributeDeleteForm


class AddCategoryEvent(events.BaseEvent):

    EVENT_TYPE_NAME = 'CategoryAdded'
    relation_key = 'categories'
    form_class = forms.ProductAddCategoryForm


class RemoveCategoryEvent(events.BaseEvent):

    EVENT_TYPE_NAME = 'CategoryRemoved'
    relation_key = 'categories'
    form_class = forms.ProductAddCategoryForm

