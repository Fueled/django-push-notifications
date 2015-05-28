# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pushdevice',
            unique_together=set([('user', 'token')]),
        ),
    ]
