# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0012_remove_show_recurrence'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='recurrence_rrule',
            field=recurrence.fields.RecurrenceField(blank=True),
        ),
    ]
