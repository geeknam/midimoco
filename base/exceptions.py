
class EntityNotCreated(Exception):
    pass


class InvalidEvent(Exception):

    def __init__(self, message, errors):
        super(InvalidEvent, self).__init__(message)
        self.errors = errors
