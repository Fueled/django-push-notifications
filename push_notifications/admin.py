# -*- coding: utf-8 -*-

# Third Party Stuff
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect

# Local
from .models import PushDevice
from .views import SendPushNotificationView


class SendPushAdmin(object):
    """
    Send Push admin is a mixin that enables the developer to give
    the admin user an extra action for sending a push notification.
    """

    actions = ['send_notification']

    def send_notification(self, request, queryset):
        """
        action used to send a custom push notification
        to selected users
        """
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        request.session['users'] = selected
        return HttpResponseRedirect("/admin/users/user/send_push")

    send_notification.short_description = 'Send push notitifcation to selected users'

    def get_urls(self):
        """
        Override the method to add our own url to the list.
        This way we don't interfere with any urls patterns.
        """
        urls = super(SendPushAdmin, self).get_urls()
        my_urls = [
            url(r'^send_push/$', SendPushNotificationView.as_view(),
                name="send-user-push"),
        ]
        return my_urls + urls


class PushDeviceAdmin(admin.ModelAdmin):
    """
    The push device admin. Displaying the token with the related user.
    """
    list_display = ['user', 'token']
    search_fields = ['user__username', 'user__first_name', 'user__last_name',
                     'user__email']


admin.site.register(PushDevice, PushDeviceAdmin)
