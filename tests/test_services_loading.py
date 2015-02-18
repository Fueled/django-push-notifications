"""
Tests for the Service loading
"""
from django.test import TestCase
from push_notifications.services import get_service
from push_notifications.services.zeropush import ZeroPushService


class TestServiceLoading(TestCase):
    service = get_service()

    # Check if service is instance of ZeroPush
    assert isinstance(service, ZeroPushService)
