# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import register_device, unregister_device

urlpatterns = patterns(
    '',
    url(r'^register/$', register_device, name='push-notifications-register'),
    url(r'^unregister/$', unregister_device, name='push-notifications-unregister')
)
