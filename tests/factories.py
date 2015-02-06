# -*- coding: utf-8 -*-

# Standard Library
import threading

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
