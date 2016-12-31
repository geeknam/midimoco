from django.dispatch import Signal

update_projection = Signal(providing_args=['event'])
