# -*- coding: utf-8 -*-

# Third party
from rest_framework import serializers


class DeviceTokenSerializer(serializers.Serializer):
    token = serializers.CharField(label='Token', min_length=32, required=True)
