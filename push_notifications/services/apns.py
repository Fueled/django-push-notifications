"""
Apple Push Notification Service
Documentation is available on the iOS Developer Library:
https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/ApplePushService.html
"""
import time
from datetime import timedelta
from apns import APNs, Frame, Payload
from django.core.exceptions import ImproperlyConfigured
from .base import BaseService


class APNSPushService(BaseService):

    def __init__(self, configuration):
        self.settings = configuration.get('APNS_CONF', {})

        self.settings.setdefault('APNS_USE_SANDBOX', False)

        use_sandbox = self.settings.get('APNS_USE_SANDBOX')
        if use_sandbox:
            cert_file = self.settings.get('APNS_CERT_SANDBOX')
        else:
            cert_file = self.settings.get('APNS_CERT_PRODUCTION')

        if not cert_file:
            raise ImproperlyConfigured(
                'You need to set DJANGO_PUSH_NOTIFICATIONS["APNS_CONF"]["APNS_CERT_PRODUCTION"]\
                 to send messages through APNS.'
            )

        try:
            with open(cert_file, "r") as f:
                f.read()
        except Exception as e:
            raise ImproperlyConfigured("The APNS certificate file at %r is not readable: %s" % (cert_file, e))

    def _get_apns_connection(self):
        use_sandbox = self.settings.get('APNS_USE_SANDBOX')
        if use_sandbox:
            cert_file = self.settings.get('APNS_CERT_SANDBOX')
        else:
            cert_file = self.settings.get('APNS_CERT_PRODUCTION')

        return APNs(use_sandbox=use_sandbox, cert_file=cert_file, enhanced=True)

    def send_push_notification(self, devices, message,
                               badge_number=None, sound=None,
                               custom=None, expiry=None,
                               category=None, content_available=False):
        """
        Sends an APNS notification to one or more devices.

        Note that if set message should always be a string. If it is not set,
        it won't be included in the notification. You will need to pass None
        to this for silent notifications.
        """
        payload = Payload(alert=message, sound=sound, badge=badge_number, custom=custom,
                          content_available=content_available, category=category)

        # add default expiry if not available
        expiry_time = expiry if expiry else timedelta(days=30).total_seconds()
        expiry = time.time() + expiry_time

        device_tokens = [device.token for device in devices]

        apns = self._get_apns_connection()

        if len(device_tokens) == 1:
            apns.gateway_server.send_notification(token_hex=device_tokens[0],
                                                  payload=payload,
                                                  expiry=expiry)
        else:
            # Bulk notification
            frame = Frame()
            identifier, expiry, priority = 1, expiry, 10
            for token in device_tokens:
                frame.add_item(token, payload, identifier, expiry, priority)

            apns.gateway_server.send_notification_multiple(frame)

        return True

    def register_push_device(self, token):
        return True

    def get_expired_device_tokens(self):
        feedback_connection = self._get_apns_connection()
        # Get feedback messages.
        tokens = []

        for (token_hex, fail_time) in feedback_connection.feedback_server.items():
            tokens.append(token_hex)

        return tokens
