# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0004_auto_20150820_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 20, 23, 3, 54, 33809)),
            preserve_default=False,
        ),
    ]
