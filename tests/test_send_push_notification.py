"""
Tests for send_push_notification methods
"""
import random

from django.test import TestCase
from push_notifications.services.zeropush import ZEROPUSH_NOTIFY_URL
import responses

from push_notifications.utils import send_push_notification
from .factories import (PushDeviceFactory, TestUserFactory,
                        request_notify_callback as request_callback)

from push_notifications.models import PushDevice


class SendPushNotificationTest(TestCase):
    @responses.activate
    def test_send_push_notification_utils(self):

        devices = PushDeviceFactory.create_batch(random.randint(1, 10))

        responses.add_callback(
            responses.POST, ZEROPUSH_NOTIFY_URL,
            callback=request_callback,
            content_type='application/json',
        )

        send = send_push_notification(devices, "HeloMoto")

        assert send is True

    @responses.activate
    def test_send_push_notification_user(self):
        user = TestUserFactory.create()
        PushDeviceFactory.create_batch(random.randint(1, 10), user=user)

        responses.add_callback(
            responses.POST, ZEROPUSH_NOTIFY_URL,
            callback=request_callback,
            content_type='application/json',
        )

        send = user.push_devices.send_push_notification("HeloMoto")

        assert send is True

    @responses.activate
    def test_send_push_notification_objects_manager(self):
        user = TestUserFactory.create()
        PushDeviceFactory.create_batch(random.randint(1, 10),
                                       user=user)
        responses.add_callback(
            responses.POST, ZEROPUSH_NOTIFY_URL,
            callback=request_callback,
            content_type='application/json',
        )

        send = PushDevice.objects.send_push_notification("HeloMoto")

        assert send is True
