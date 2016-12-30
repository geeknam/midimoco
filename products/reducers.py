from base.reducers import BaseReducer


class Reducer(BaseReducer):

    def on_category_added(self, aggregate, next_event):
        aggregate.setdefault(
            self.model.add_category_event.relation_key, []
        ).append(next_event.data)
        return aggregate

    def on_category_removed(self, aggregate, next_event):
        aggregate.get(
            self.model.remove_category_event.relation_key, []
        ).remove(next_event.data)
        return aggregate
