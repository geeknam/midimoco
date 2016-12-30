from django import forms
from base.forms import BaseUpdateEventForm, BaseAttributeDeleteForm
from django.utils.text import slugify


class ProductForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField()
    price = forms.DecimalField(
        min_value=0, decimal_places=2
    )


class ProductUpdateForm(BaseUpdateEventForm):
    entity_id = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(required=False)
    price = forms.DecimalField(
        min_value=0, decimal_places=2,
        required=False
    )


class ProductDeleteForm(BaseUpdateEventForm):
    pass


class ProductAttributeDeleteForm(BaseAttributeDeleteForm):

    ALLOWED_ATTRIBUTES = (
        ('description', 'description'),
        ('entity_id', 'entity_id')
    )


class ProductAddCategoryForm(BaseUpdateEventForm):

    category = forms.CharField(max_length=100)

    def clean(self):
        self.cleaned_data = super(ProductAddCategoryForm, self).clean()
        category_slug = slugify(self.cleaned_data['category'])
        self.cleaned_data.update({
            'category_slug': category_slug
        })
        return self.cleaned_data
