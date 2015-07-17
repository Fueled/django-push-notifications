# -*- coding: utf-8 -*-

# Third party
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.views.generic import FormView
from django.contrib.auth import get_user_model

# Local
from .models import PushDevice
from .serializers import DeviceTokenSerializer
from .forms import PushNotificationForm


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
            device = PushDevice.register_push_device(
                request.user, serializer.validated_data['token'])
            registered = (True if device is not None else False)
            status_code = (200 if registered is True else 400)
            return Response({'registered': registered}, status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPushNotificationView(FormView):
    """
    form view that allows the sending of a custom
    message to a selecion of users through the django
    admin, utilizing django actions
    """
    template_name = 'send_push_form.html'
    form_class = PushNotificationForm
    success_url = '/admin/users/user'

    def form_valid(self, form):
        user_ids = self.request.session.get('users')
        users = get_user_model().objects.filter(pk__in=user_ids)

        alert = form.cleaned_data.get('message')
        badge = form.cleaned_data.get('badge')
        sound = form.cleaned_data.get('sound', None)
        info = form.cleaned_data.get('info', None)

        # Flatten out the devices, this will speed up the time spending
        # on sending the push notification when we do it per user.
        devices = []
        for user in users:
            devices += user.push_devices.all()

        PushDevice.send_push_notification(devices, alert, badge_number=badge,
                                          sound=sound, payload=info)

        del self.request.session['users']
        return super(SendPushNotificationView, self).form_valid(form)
