# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import RegisterDeviceView, UnRegisterDeviceView

urlpatterns = patterns(
    '',
    url(r'^register/$', RegisterDeviceView.as_view(),
        name='push-notifications-register'),
    url(r'^unregister/$', UnRegisterDeviceView.as_view(),
        name='push-notifications-unregister')
)
