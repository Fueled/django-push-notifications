"""
Tests for registering a device
"""
from django.test import TestCase
from uuid import uuid4

# Local stuff
from .factories import TestUserFactory
from push_notifications.models import PushDevice
from push_notifications.utils import register_push_device


class RegisterDeviceTests(TestCase):
    def _create_token(self):
        return uuid4()

    def _create_user(self):
        return TestUserFactory.create()

    def test_register_device_manager(self):
        """
        Test if register_device() on the manager works as expected
        """
        user = TestUserFactory.create()
        device = PushDevice.objects.register_push_device(
            user, self._create_token())

        assert device is not None
        assert device.user.pk == user.pk

    def test_register_device_manager_notify_types(self):
        """
        Test if manager.register_push_device() accepts notify_types
        """
        user = self._create_user()
        device = PushDevice.objects.register_push_device(
            user, self._create_token(), notify_types='likes')

        notification = device.notification_settings.first()
        assert device.notification_settings.count() == 1
        assert notification.name == 'likes'

        device = PushDevice.objects.register_push_device(
            user, self._create_token(), notify_types=['likes', 'comments'])

        assert device.notification_settings.count() == 2

        notification_likes = device.notification_settings.filter(name='likes').first()
        assert notification_likes.send is True

        notification_comments = device.notification_settings.filter(name='comments').first()
        assert notification_comments.send is True

    def test_register_device_service(self):
        """
        Tests if register_push_device in services works as expected
        """
        user = self._create_user()
        device = register_push_device(user, self._create_token())

        assert device is not None
        assert device.user.pk == user.pk

    def test_register_device_service_notify_types(self):
        """
        Tests if register_push_device in services workw with extra
        notice_types
        """
        user = self._create_user()
        device = register_push_device(user, self._create_token(), notice_types='likes')

        # Check if notice_types has 'likes' in it
        notification = device.notification_settings.first()
        assert device.notification_settings.count() == 1
        assert notification.name == 'likes'
        assert notification.send is True

        # Test with multiple notice_types
        device = register_push_device(user, self._create_token(),
                                      notice_types=['likes', 'comments'])

        # Check if notice_types has 'likes' and 'comments'
        assert device.notification_settings.count() == 2

        notification_likes = device.notification_settings.filter(name='likes').first()
        assert notification_likes.send is True

        notification_comments = device.notification_settings.filter(name='comments').first()
        assert notification_comments.send is True
