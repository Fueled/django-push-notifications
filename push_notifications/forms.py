# -*- coding: utf-8 -*-
import json

# Third Party Stuff
from django import forms


class PushNotificationForm(forms.Form):
    message = forms.CharField()
    badge = forms.BooleanField(required=False)
    sound = forms.CharField(required=False)
    info = forms.CharField(
        required=False, widget=forms.Textarea,
        error_messages={'invalid_json': 'Please enter your name'})

    def clean_info(self):
        """
        Checks if info is in a valid json format.
        """
        # Make sure value is not an object when
        # value is empty
        value = (self.cleaned_data['info'] if self.cleaned_data['info'] else "{}")
        try:
            self.cleaned_data['info'] = json.loads(value)
        except ValueError:
            raise forms.ValidationError(
                "Info payload is in an invalid JSON format.")
