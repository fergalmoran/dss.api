# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0013_show_recurrence_rrule'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='recurrence',
            field=models.SmallIntegerField(default=2),
            preserve_default=False,
        ),
    ]
