# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Notification name')),
                ('send', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PushDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=255, verbose_name='Device token string', db_index=True)),
                ('device_type', models.CharField(max_length=255, null=True, verbose_name='Type of device', blank=True)),
                ('user', models.ForeignKey(related_name='push_devices', verbose_name='Owner of this device', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='notificationsetting',
            name='device',
            field=models.ForeignKey(related_name='notification_settings', to='push_notifications.PushDevice'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='notificationsetting',
            unique_together=set([('device', 'name')]),
        ),
    ]
