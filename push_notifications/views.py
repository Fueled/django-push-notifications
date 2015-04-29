# -*- coding: utf-8 -*-

# Third party
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Local
from .models import PushDevice
from .serializers import DeviceTokenSerializer


class UnRegisterDeviceView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = DeviceTokenSerializer(data=request.data)
        # check whether it's valid:
        if serializer.is_valid():
            PushDevice.unregister_push_device(
                request.user, serializer.validated_data['token'])
            return Response({'unregistered': True})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterDeviceView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = DeviceTokenSerializer(data=request.data)
        # check whether it's valid:
        if serializer.is_valid():
            PushDevice.register_push_device(
                request.user, serializer.validated_data['token'])
            return Response({'registered': True})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
