# -*- coding: utf-8 -*-
from uuid import uuid4

# Third party stuff
from django.test import TestCase, RequestFactory

# Local
from .factories import TestUserFactory, PushDeviceFactory
from push_notifications.views import register_device, unregister_device


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = TestUserFactory.create()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_register_device(self):
        push_device = PushDeviceFactory.build()
        data = {
            'token': push_device.token
        }
        self.assertEqual(
            self.user.push_devices.filter(token=data['token']).count(), 0)

        request = self.factory.post('/register', data)
        request.user = self.user

        response = register_device(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.user.push_devices.filter(token=data['token']).count(), 1)

    def test_unregister_device(self):
        push_device = PushDeviceFactory.create(user=self.user)
        data = {
            'token': push_device.token
        }
        self.assertEqual(
            len(self.user.push_devices.filter(token=data['token'])), 1)

        request = self.factory.post('/unregister', data)
        request.user = self.user

        response = unregister_device(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.user.push_devices.filter(token=data['token']).count(), 0)

    def test_register_device_unauthorized(self):
        # Check if authorization is required for the register endpoint
        data = {
            'token': uuid4()
        }
        request = self.factory.post('/register', data)

        response = register_device(request)
        self.assertEqual(response.status_code, 403)

    def test_unregister_device_unauthorized(self):
        # Check if authorization is required for the register endpoint
        data = {
            'token': uuid4()
        }
        request = self.factory.post('/unregister', data)

        response = register_device(request)
        self.assertEqual(response.status_code, 403)

    def test_validation_errors_register_device(self):
        # Check if authorization is required for the register endpoint
        data = {
            'not': 'Working',
            'token': 'iswaytooshort'
        }
        request = self.factory.post('/unregister', data)
        request.user = self.user

        response = register_device(request)
        self.assertEqual(response.status_code, 400)
