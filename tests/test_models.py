"""
Tests for the PushDevice Model
"""

from django.test import TestCase

# Local stuff
from .factories import PushDeviceFactory


class ModelTest(TestCase):
    def test_required_variables(self):
        """
        Test if the model has the required properties
        """
        device = PushDeviceFactory.create()

        assert hasattr(device, 'token')
        assert hasattr(device, 'user')
