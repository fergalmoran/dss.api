# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0021_auto_20151112_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mix',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mix',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
