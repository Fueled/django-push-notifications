"""
Tests for the NotificationSettings model
"""

from django.test import TestCase

# Local stuff
from .factories import PushDeviceFactory, NotificationSettingFactory
from push_notifications.models import NotificationSetting


class NotificationSettingsTest(TestCase):
    def test_required_variables(self):
        """
        Test if the model has the required properties
        """
        notification_settings = NotificationSettingFactory.create()

        assert hasattr(notification_settings, 'device')
        assert hasattr(notification_settings, 'name')
        assert hasattr(notification_settings, 'send')

    def test_can_send_method(self):
        """
        Test the can_send method on the
        NotifciationSetting works as expected
        """
        device = PushDeviceFactory.create()
        notification_setting = NotificationSettingFactory.create(
            device=device)
        can_send = NotificationSetting.can_send(device,
                                                notification_setting.name)

        # The notification.send setting must be equal
        assert can_send == notification_setting.send
