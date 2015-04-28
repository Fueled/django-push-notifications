# -*- coding: utf-8 -*-

# Third party
from django import forms


class PushDeviceForm(forms.Form):
    token = forms.CharField(label='Token', max_length=64, min_length=64,
                            required=True)
