# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0003_auto_20150820_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='description',
            field=models.CharField(max_length=2048, default='New Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='recurrence',
            field=models.CharField(max_length=30, default='R'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='show',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 20, 22, 57, 40, 815435)),
            preserve_default=False,
        ),
    ]
