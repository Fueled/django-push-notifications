from django.core.exceptions import ImproperlyConfigured
import requests
from datetime import timedelta, datetime

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
        if len(devices):
            params = {
                "auth_token": self.auth_token,
                "device_tokens[]": [device.token for device in devices],
                "expiry": expiry,
                "sound": sound,
                "info": payload
            }

            for key in params.keys():
                if not params[key]:
                    del params[key]

            expiry_time = timedelta(days=30).seconds

            if isinstance(expiry, datetime):
                expiry_time = expiry.second
            elif isinstance(expiry, timedelta):
                expiry_time = expiry.seconds

            params['expiry'] = expiry_time

            response = requests.post(ZEROPUSH_REQUEST_URL, params)

            if response.ok:
                return True
        return False
