from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import requests

from .base import BaseService


class ZeroPushService(BaseService):

    def __init__(self):
        try:
            configuration = settings.DJANGO_PUSH_NOTIFICATION
        except AttributeError:
            raise ImproperlyConfigured('There are no Django Push '
                                       'Notifications set up')

        self.auth_token = configuration.get('AUTH_TOKEN')

        if not self.auth_token:
            raise ImproperlyConfigured('For ZeroPush to work we need an '
                                       'AUTH_TOKEN in the configuration')

    def send_push_notification(devices, message,
                               badge_number=None, sound=None,
                               payload=None, expiry=None):
        # Create the payload
        payload = {
            'message': message,
            'badge': badge_number,
            'sound': sound,
            'info': payload,
            'expiry': expiry
        }

        requests.post()
        pass
