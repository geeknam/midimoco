import json

from django.contrib import admin
from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter


class JsonPrettifyMixin(object):

    def data_prettified(self, instance):
        # Convert the data to sorted, indented JSON
        data = getattr(instance, self.json_prettify_field)
        json_data = json.dumps(data, sort_keys=True, indent=4)
        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')
        # Highlight the data
        response = highlight(json_data, JsonLexer(), formatter)
        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        # Safe the output
        return mark_safe(style + response)

    data_prettified.short_description = 'data prettified'


class BaseEventAdmin(JsonPrettifyMixin, admin.ModelAdmin):
    exclude = ('data',)
    readonly_fields = (
        'entity_id',
        'checkpoint',
        'event_type',
        'created_at',
        'data_prettified'
    )
    list_filter = ('event_type',)
    json_prettify_field = 'data'


class BaseProjectionAdmin(JsonPrettifyMixin, admin.ModelAdmin):
    readonly_fields = (
        'entity_id',
        'checkpoint',
        'data_prettified'
    )
    json_prettify_field = 'view'
