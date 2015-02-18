from django.core.exceptions import ImproperlyConfigured
import requests
import json

from .base import BaseService

ZEROPUSH_REQUEST_URL = 'https://api.zeropush.com/notify'


class ZeroPushService(BaseService):

    def __init__(self, settings):
        self.auth_token = settings.get('AUTH_TOKEN')

        if not self.auth_token:
            raise ImproperlyConfigured('For ZeroPush to work you need an '
                                       'AUTH_TOKEN in the configuration')

    def send_push_notification(self, devices, message,
                               badge_number=None, sound=None,
                               payload=None, expiry=None):
        params = {
            "auth_token": self.auth_token,
            "device_tokens[]": [device.token for device in devices]
        }
        if message is not None:
            params.update({"alert": message})
        if sound is not None:
            params.update({"sound": sound})
        if badge_number is not None:
            params.update({"badge_number": badge_number})
        if payload is not None:
            params.update({"info": json.dumps(payload)})

        response = requests.post(ZEROPUSH_REQUEST_URL, params)

        if response.ok:
            return True

        return False
