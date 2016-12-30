import re

re_camel_case = re.compile(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))')


def camel_case_to_spaces(value):
    """
    Splits CamelCase and converts to lower case. Also strips leading and
    trailing whitespace.
    """
    return re_camel_case.sub(r'_\1', value).strip('_').lower()


class BaseReducer(object):

    def contribute_to_class(self, model, name):
        self.name = name
        self.model = model
        setattr(model, name, self)

    def reduce(self, aggregate, next_event):
        event_name = camel_case_to_spaces(next_event.event_type)
        handler = getattr(self, 'on_%s' % event_name, None)
        if handler:
            return handler(aggregate, next_event)
        return aggregate

    def on_created(self, aggregate, next_event):
        return next_event.data

    def on_updated(self, aggregate, next_event):
        aggregate.update(next_event.data)
        return aggregate

    def on_attribute_deleted(self, aggregate, next_event):
        for attr in next_event.data.get('attributes', []):
            aggregate.pop(attr, None)
        return aggregate

    def on_deleted(self, aggregate, next_event):
        if next_event.event_type == self.model.delete_event.EVENT_TYPE_NAME:
            raise self.model.DoesNotExist(
                'Entity deleted on %s' % next_event.created_at)
