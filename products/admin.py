from django.contrib import admin
from base.admin import BaseEventAdmin, BaseProjectionAdmin
from products.models import ProductEvent, ProductProjection


@admin.register(ProductEvent)
class ProductEventAdmin(BaseEventAdmin):
    pass


@admin.register(ProductProjection)
class ProductProjectionAdmin(BaseProjectionAdmin):
    pass
