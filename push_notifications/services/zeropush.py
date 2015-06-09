import json
from datetime import timedelta, datetime

from django.core.exceptions import ImproperlyConfigured
import requests

from .base import BaseService

ZEROPUSH_REQUEST_URL = 'https://api.zeropush.com/'
ZEROPUSH_NOTIFY_URL = ZEROPUSH_REQUEST_URL + 'notify'
ZEROPUSH_REGISTER_URL = ZEROPUSH_REQUEST_URL + 'register'


class ZeroPushService(BaseService):

    def __init__(self, settings):
        self.auth_token = settings.get('AUTH_TOKEN')

        if not self.auth_token:
            raise ImproperlyConfigured('For ZeroPush to work you need an '
                                       'AUTH_TOKEN in the configuration')

    @staticmethod
    def process_expiry(expiry):
        """
        Processes the expiry, checks if it's a datetime or timedelta and
        responds accordingly
        """
        if isinstance(expiry, datetime):
            expiry = expiry.second

        if isinstance(expiry, timedelta):
            expiry = expiry.seconds
        return expiry

    def get_auth_headers(self):
        return {
            'Authorization': 'Token token="{}"'.format(self.auth_token)
        }

    def send_push_notification(self, devices, message,
                               badge_number=None, sound=None,
                               payload=None, expiry=None):
        """
        Sends a push notification request to ZeroPush.
        """
        if len(devices):
            params = {
                "auth_token": self.auth_token,
                "device_tokens[]": [device.token for device in devices]
            }

            if message is not None:
                params.update({"alert": message})

            if sound is not None:
                params.update({"sound": sound})

            if badge_number is not None:
                params.update({"badge": badge_number})

            if payload is not None:
                params.update({"info": json.dumps(payload)})

            if expiry is not None:
                expiry = self.process_expiry(expiry)
                params.update({'expiry': expiry})

            response = requests.post(ZEROPUSH_NOTIFY_URL, params,
                                     headers=self.get_auth_headers())

            if response.ok:
                return True
        return False

    def register_push_device(self, token):
        """
        Registers a push device on zeropush.
        """
        params = {
            'device_token': token
        }

        response = requests.post(ZEROPUSH_REGISTER_URL, params,
                                 headers=self.get_auth_headers())
        if response.ok:
            return True

        return False
