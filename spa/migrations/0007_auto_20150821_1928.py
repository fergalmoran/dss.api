# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0006_auto_20150820_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='show',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
