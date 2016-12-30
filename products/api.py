
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from products.models import ProductEvent, ProductProjection


class ProductResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'entity_id',
        'title': 'view.title',
        'description': 'view.description',
        'price': 'view.price',
        'categories': 'view.categories'
    })

    def list(self):
        return ProductProjection.objects.all()

    def detail(self, pk):
        return ProductProjection.objects.get(entity_id=pk)

    def create(self):
        event = ProductEvent.events_manager.create_event.save(self.data)
        return ProductProjection.objects.get(
            entity_id=event.entity_id
        )

    def update(self, pk):
        self.data['entity_id'] = pk
        event = ProductEvent.events_manager.update_event.save(self.data)
        return ProductProjection.objects.get(
            entity_id=event.entity_id
        )

    def delete(self, pk):
        self.data['entity_id'] = pk
        ProductEvent.events_manager.delete_event.save(self.data)

