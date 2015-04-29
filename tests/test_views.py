# -*- coding: utf-8 -*-
from uuid import uuid4

# Third party stuff
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from django.test.client import RequestFactory

# Local
from .factories import TestUserFactory, PushDeviceFactory
from push_notifications.views import RegisterDeviceView, UnRegisterDeviceView


class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = TestUserFactory.create()
        self.factory = RequestFactory()
        self.register_view = RegisterDeviceView.as_view()
        self.unregister_view = UnRegisterDeviceView.as_view()

    def test_register_device(self):
        push_device = PushDeviceFactory.build(user=self.user)
        data = {
            'token': push_device.token
        }
        request = self.factory.post('/accounts/django-superstars/', data)
        force_authenticate(request, user=self.user)
        response = self.register_view(request)
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
        force_authenticate(request, user=self.user)

        response = self.unregister_view(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.user.push_devices.filter(token=data['token']).count(), 0)

    def test_register_device_unauthorized(self):
        # Check if authorization is required for the register endpoint
        data = {
            'token': uuid4()
        }
        request = self.factory.post('/register', data)

        response = self.register_view(request)
        self.assertEqual(response.status_code, 403)

    def test_unregister_device_unauthorized(self):
        # Check if authorization is required for the register endpoint
        data = {
            'token': uuid4()
        }
        request = self.factory.post('/unregister', data)

        response = self.register_view(request)
        self.assertEqual(response.status_code, 403)

    def test_validation_errors_register_device(self):
        # Check if authorization is required for the register endpoint
        data = {
            'not': 'Working',
            'token': 'iswaytooshort'
        }
        request = self.factory.post('/unregister', data)
        force_authenticate(request, user=self.user)

        response = self.register_view(request)
        self.assertEqual(response.status_code, 400)
