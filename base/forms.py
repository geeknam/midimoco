from django import forms


class BaseUpdateEventForm(forms.Form):

    entity_id = forms.CharField(max_length=100)

    def clean(self):
        # remove entity id on update or delete
        self.cleaned_data.pop('entity_id', None)
        return self.cleaned_data


class BaseAttributeDeleteForm(forms.Form):

    ALLOWED_ATTRIBUTES = ()

    entity_id = forms.CharField(max_length=100)
    attributes = forms.MultipleChoiceField(
        choices=ALLOWED_ATTRIBUTES
    )
