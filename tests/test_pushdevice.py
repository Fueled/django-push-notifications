"""
Tests for the PushDevice Model
"""
import random

from django.test import TestCase

# Local stuff
from .factories import PushDeviceFactory, TestUserFactory
from push_notifications.models import NotificationSetting, PushDevice


SETTING_LIKE = 'like'
SETTING_COMMENT = 'comments'


class PushDeviceTest(TestCase):
    def test_required_variables(self):
        """
        Test if the model has the required properties
        """
        device = PushDeviceFactory.create()

        assert hasattr(device, 'token')
        assert hasattr(device, 'user')

    def test_add_permission(self):
        """
        Test if PushDevice.add_permissions() works as expected.
        """
        device = PushDeviceFactory.create()

        # Add one
        device.add_permissions(SETTING_LIKE)

        # Check if this one is persisted
        notification_setting = NotificationSetting.objects.filter(
            device=device, name=SETTING_LIKE).first()
        assert notification_setting.send is True

        # Add one again, same name
        device.add_permissions(SETTING_LIKE)
        notification_settings = NotificationSetting.objects.filter(
            device=device, name=SETTING_LIKE)
        assert notification_settings.count() == 1

    def test_add_multiple_permissions(self):
        """
        Test if PushDevice.add_permissions() works with a list
        """
        device = PushDeviceFactory.create()

        # Add multiple permissions
        device.add_permissions([SETTING_LIKE, SETTING_COMMENT])

        # Check if the two are persisted
        notification_settings = NotificationSetting.objects.filter(
            device=device)
        assert notification_settings.count() == 2

        assert notification_settings.first().send is True
        assert notification_settings.last().send is True

    def test_remove_permission(self):
        """
        Test if PushDevice.remove_permission() works as expected.
        """
        device = PushDeviceFactory.create()

        # Add one
        device.add_permissions(SETTING_LIKE)

        assert NotificationSetting.objects.get(device=device,
                                               name=SETTING_LIKE).send is True

        # Remove it
        device.remove_permissions(SETTING_LIKE)

        assert NotificationSetting.objects.get(device=device,
                                               name=SETTING_LIKE).send is False

    def test_bulk_permissions(self):
        """
        Test if ForeignKey add_permissions works
        """
        user = TestUserFactory.create()
        PushDeviceFactory.create_batch(random.randint(0, 10), user=user)

        user.push_devices.add_permissions(SETTING_LIKE)

        for device in user.push_devices.all():
            notification = NotificationSetting.objects.filter(
                device=device, name=SETTING_LIKE).first()
            assert notification.send is True
            assert notification.name == SETTING_LIKE

    def test_mutliple_bulk_permissions(self):
        """
        Test if ForeignKey add_permissions works
        """
        user = TestUserFactory.create()
        PushDeviceFactory.create_batch(random.randint(0, 10), user=user)

        user.push_devices.add_permissions([SETTING_LIKE, SETTING_COMMENT])

        for device in user.push_devices.all():
            notifications = NotificationSetting.objects.filter(
                device=device, name__in=[SETTING_LIKE, SETTING_COMMENT])
            assert notifications[0].send is True
            assert notifications[0].name in [SETTING_LIKE, SETTING_COMMENT]

    def test_remove_permissions(self):
        """
        Test if ForeignKey remove_permissions works
        """
        user = TestUserFactory.create()
        PushDeviceFactory.create_batch(random.randint(0, 10), user=user)

        user.push_devices.remove_permissions(SETTING_LIKE)

        for device in user.push_devices.all():
            notification = NotificationSetting.objects.filter(
                device=device, name=SETTING_LIKE).first()
            assert notification.send is False
            assert notification.name == SETTING_LIKE

    def test_pushdevice_objects_add_permissions(self):
        """
        Test if PushDevice.objects add_permissions works
        """
        user = TestUserFactory.create()
        PushDeviceFactory.create_batch(random.randint(0, 10), user=user)

        PushDevice.objects.filter(user=user).add_permissions(SETTING_LIKE)

        for notification in NotificationSetting.objects.filter(
                device__user=user).all():
            assert notification.send is True
            assert notification.name == SETTING_LIKE

    def test_pushdevice_objects_remove_permissions(self):
        """
        Test if PushDevice.objects remove_permissions works
        """
        user = TestUserFactory.create()
        PushDeviceFactory.create_batch(random.randint(0, 10), user=user)

        PushDevice.objects.filter(user=user).remove_permissions(SETTING_LIKE)

        for notification in NotificationSetting.objects.filter(
                device__user=user).all():
            assert notification.send is False
            assert notification.name == SETTING_LIKE

    def test_with_permission_filter(self):
        """
        Test if with_permission() filters as expected
        """
        user = TestUserFactory.create()
        like_devices = PushDeviceFactory.create_batch(random.randint(1, 10),
                                                      user=user)

        PushDevice.objects.filter(user=user).add_permissions(SETTING_LIKE)

        # Make objects without permission
        PushDeviceFactory.create_batch(random.randint(1, 10), user=user)

        assert user.push_devices.with_permission(SETTING_LIKE).count() == len(like_devices)
