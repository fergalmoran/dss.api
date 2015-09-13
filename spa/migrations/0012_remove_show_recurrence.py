# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0011_auto_20150910_1927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='show',
            name='recurrence',
        ),
    ]
