from base.exceptions import InvalidEvent


class BaseEvent(object):

    def __init__(self, name=None):
        self.name = name
        self.model = None
        self.entity_id = None

    def contribute_to_class(self, model, name):
        if not self.name:
            self.name = name
        self.model = model
        setattr(model, name, self)

    @property
    def manager(self):
        return self.model.events_manager

    def get_checkpoint(self):
        return self.manager.get_last_checkpoint(self.entity_id) + 1

    def validate(self, payload):
        form = self.form_class(payload)
        if not form.is_valid():
            raise InvalidEvent(
                message='%s event on %s failed' % (
                    self.EVENT_TYPE_NAME,
                    self.model.__class__.__name__
                ),
                errors=form.errors
            )
        return form.cleaned_data

    def get_event(self, payload):
        return {
            'entity_id': self.entity_id,
            'checkpoint': self.get_checkpoint(),
            'event_type': self.EVENT_TYPE_NAME,
            'data': payload
        }

    def save(self, payload):
        cleaned_data = self.validate(payload)
        self.entity_id = payload.get('entity_id')
        return self.manager.create(
            **self.get_event(cleaned_data)
        )


class BaseCreateEvent(BaseEvent):

    EVENT_TYPE_NAME = 'Created'

    def get_event(self, payload):
        return {
            # Creation always start with checkpoint of 0
            'checkpoint': 0,
            'event_type': self.EVENT_TYPE_NAME,
            'data': payload
        }


class BaseUpdateEvent(BaseEvent):

    EVENT_TYPE_NAME = 'Updated'


class BaseDeleteEvent(BaseEvent):

    EVENT_TYPE_NAME = 'Deleted'


class BaseAttributeDeleteEvent(BaseDeleteEvent):

    EVENT_TYPE_NAME = 'AttributeDeleted'
