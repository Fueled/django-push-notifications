from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class PushDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_("Owner of this device"))
    token = models.CharField(_("Device token string"),
                             max_length=255, db_index=True)
    device_type = models.CharField(_("Type of device"),
                                   max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u"Device %s" % self.token


class NotificationSetting(models.Model):
    device = models.ForeignKey(PushDevice, related_name='notification_settings')
    name = models.CharField(max_length=255, verbose_name=_("Notification name"))
    send = models.BooleanField(default=True)

    class Meta:
        unique_together = ('device', 'name')

    def __unicode__(self):
        return "{0} - {1}".format(self.device, self.type)

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
