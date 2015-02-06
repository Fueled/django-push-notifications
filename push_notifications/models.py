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
