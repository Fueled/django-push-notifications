from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.query import QuerySet

from .services import get_service


class PushDeviceMethods(object):
    def add_permissions(self, notice_types):
            self.model.batch_change_permissions(
                notice_types, self.all(), send=True)

    def remove_permissions(self, notice_types):
        self.model.batch_change_permissions(
            notice_types, self.all(), send=False)

    def register_push_device(self, user, token, notify_types=None):
        return self.model.register_push_device(user, token, notify_types)

    def send_push_notification(self, message, **kwargs):
        return self.model.send_push_notification(self.all(),
                                                 message, **kwargs)

    def with_permission(self, permission):
        return self.filter(notification_settings__name=permission,
                           notification_settings__send=True)

    def with_permissions(self, permissions):
        return self.filter(notification_settings__name__in=permissions,
                           notification_settings__send=True)

    def unregister_push_device(self, user, token):
        return self.model.unregister_push_device(user, token)


class PushDeviceManager(PushDeviceMethods, models.Manager):

    # This enables us to have add_permissions on the
    # RelatedManager
    use_for_related_fields = True

    def get_queryset(self):
        return self.model.QuerySet(self.model)


class PushDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_("Owner of this device"),
                             related_name="push_devices")
    token = models.CharField(_("Device token string"),
                             max_length=255, db_index=True)
    device_type = models.CharField(_("Type of device"),
                                   max_length=255, blank=True, null=True)

    objects = PushDeviceManager()

    class Meta:
        unique_together = ('user', 'token')

    def add_permissions(self, notice_types):
        """ Adds a permission to the push device """
        PushDevice.change_permissions(notice_types, self, send=True)

    def remove_permissions(self, notice_types):
        """ Removes a permission to the push device """
        PushDevice.change_permissions(notice_types, self, send=False)

    @classmethod
    def register_push_device(cls, user, token, notice_types=None):
        registered = get_service().register_push_device(token)

        if not registered:
            return None

        # Delete any devices with the same token.
        cls.objects.filter(token=token).delete()

        device, created = cls.objects.get_or_create(user=user, token=token)

        if notice_types:
            cls.change_permissions(notice_types, device)
        return device

    @classmethod
    def unregister_push_device(cls, user, token):
        deleted = user.push_devices.filter(token=token).delete()
        return deleted > 0

    @classmethod
    def change_permissions(cls, notice_types, device, send=True):
        notice_types = (notice_types
                        if isinstance(notice_types, list) else [notice_types])

        for notice_type in notice_types:
            try:
                notification_setting = NotificationSetting.objects.get(
                    device=device, name=notice_type)
                notification_setting.send = send
                notification_setting.save()
            except NotificationSetting.DoesNotExist:
                notification_setting = NotificationSetting.objects.create(
                    device=device, name=notice_type, send=send)

    @classmethod
    def batch_change_permissions(cls, notice_types, devices, send=True):
        for device in devices:
            cls.change_permissions(notice_types, device, send)

    @classmethod
    def send_push_notification(cls, devices, message, **kwargs):
        return get_service().send_push_notification(devices, message, **kwargs)

    class QuerySet(PushDeviceMethods, QuerySet):
        pass

    def __unicode__(self):
        return u"Device %s" % self.token


class NotificationSetting(models.Model):
    device = models.ForeignKey(PushDevice, related_name='notification_settings')
    name = models.CharField(max_length=255, verbose_name=_("Notification name"))
    send = models.BooleanField(default=True)

    class Meta:
        unique_together = ('device', 'name')

    def __unicode__(self):
        return "{0} - {1}".format(self.device, self.name)

    @classmethod
    def can_send(cls, device, notice_type):
        """
        Check if the given device has the given `notice_type` enabled
        """
        try:
            notification_setting = cls.objects.get(device=device,
                                                   name=notice_type)
        except cls.DoesNotExist:
            notification_setting = cls.objects.create(device=device,
                                                      name=notice_type)

        return notification_setting.send
