"""
Tests for the ZeroPushService
"""
import responses
import json
from datetime import timedelta, datetime


from django.test import TestCase
from querystring_parser import parser as querystring_parser

# Local stuff
from .factories import PushDeviceFactory
from push_notifications.services.zeropush import ZeroPushService
from push_notifications.services.zeropush import ZEROPUSH_REQUEST_URL
from django.core.exceptions import ImproperlyConfigured
from .support.validation import validate_zeropush_payload


class ZeroPushServiceTest(TestCase):

    def test_settings_improperly_configure(self):
        # It must give an attribute error when settings are not set
        try:
            zeropush = ZeroPushService({})

            # This shouldn't be happening
            assert zeropush is None
        except ImproperlyConfigured:
            pass

        # It should run without problems, when valid settings are set
        zeropush = ZeroPushService({
            'AUTH_TOKEN': '123123'
        })

        assert isinstance(zeropush, ZeroPushService)

    @responses.activate
    def test_send_push_notification(self):

        # Make a mock of the response
        def request_callback(request):
            payload = querystring_parser.parse(request.body)

            if validate_zeropush_payload(payload):
                response_body = {
                    "sent_count": len(payload['device_tokens']['']),
                    "inactive_tokens": [],
                    "unregistered_tokens": []
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                return (200, headers, json.dumps(response_body))
            else:
                return (400, {}, {})

        responses.add_callback(
            responses.POST, ZEROPUSH_REQUEST_URL,
            callback=request_callback,
            content_type='application/json',
        )

        zeropush = ZeroPushService({
            'AUTH_TOKEN': '123123'
        })
        devices = PushDeviceFactory.create_batch(10)
        send = zeropush.send_push_notification(devices, 'This is the message',
                                               sound="annoyingSound.mp3",
                                               badge_number=1,
                                               payload={
                                                   "extra": "payload",
                                                   "in": "notification"
                                               },
                                               expiry=timedelta(days=30))

        assert send is True

    @responses.activate
    def test_zeropush_datetime_expiry(self):
        """
        Test if ZeroPush Service also accepts datetime objects
        """

        # Make a mock of the response
        def request_callback(request):
            payload = querystring_parser.parse(request.body)

            if validate_zeropush_payload(payload):
                response_body = {
                    "sent_count": len(payload['device_tokens']['']),
                    "inactive_tokens": [],
                    "unregistered_tokens": []
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                return (200, headers, json.dumps(response_body))
            else:
                return (400, {}, {})

        responses.add_callback(
            responses.POST, ZEROPUSH_REQUEST_URL,
            callback=request_callback,
            content_type='application/json',
        )

        zeropush = ZeroPushService({
            'AUTH_TOKEN': '123123'
        })
        devices = PushDeviceFactory.create_batch(10)
        send = zeropush.send_push_notification(devices, 'This is the message',
                                               sound="annoyingSound.mp3",
                                               badge_number=1,
                                               payload={
                                                   "extra": "payload",
                                                   "in": "notification"
                                               },
                                               expiry=datetime.now())
        assert send is True
