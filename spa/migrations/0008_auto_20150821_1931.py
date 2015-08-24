# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0007_auto_20150821_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='end_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
