# -*- coding: utf-8 -*-
from __future__ import absolute_import


class BaseService(object):

    def __init__(self, configuration):
        pass

    def send_push_notification(self, devices, message,
                               badge_number=None, sound=None,
                               payload=None, expiry=None):
        pass

    def register_push_device(self, token):
        return True
