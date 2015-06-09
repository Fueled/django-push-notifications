# -*- coding: utf-8 -*-

# Standard Library
import threading
import random
import json
import urlparse

# Third Party Stuff
import factory
from factory import fuzzy


class Factory(factory.DjangoModelFactory):

    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True

    _SEQUENCE = 1
    _SEQUENCE_LOCK = threading.Lock()

    @classmethod
    def _setup_next_sequence(cls):
        with cls._SEQUENCE_LOCK:
            cls._SEQUENCE += 1
        return cls._SEQUENCE


class TestUserFactory(Factory):
    class Meta:
        model = 'tests.TestUser'
        strategy = factory.CREATE_STRATEGY

    username = factory.Sequence(lambda n: "User {0}".format(n + 1))


class PushDeviceFactory(Factory):
    class Meta:
        model = 'push_notifications.PushDevice'
        strategy = factory.CREATE_STRATEGY

    token = fuzzy.FuzzyText(chars='01234567890abcdef-', length=64)
    user = factory.SubFactory('tests.factories.TestUserFactory')


class NotificationSettingFactory(Factory):
    class Meta:
        model = 'push_notifications.NotificationSetting'
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Name {0}".format(n + 1))
    device = factory.SubFactory('tests.factories.PushDeviceFactory')
    send = random.choice([True, False])


# Make a mock of the response
def request_notify_callback(request):
    payload = dict(urlparse.parse_qsl(request.body))
    response_body = {
        "sent_count": len(payload['device_tokens[]']),
        "inactive_tokens": [],
        "unregistered_tokens": []
    }
    headers = {
        'Content-Type': 'application/json'
    }
    return (200, headers, json.dumps(response_body))


# Make a mock of the response of registering a device
def request_register_callback(request):
    response_body = {
        "message": "ok"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    return (200, headers, json.dumps(response_body))
