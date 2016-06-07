# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0026_notification_notification_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_text',
            field=models.CharField(max_length=2048),
        ),
    ]
