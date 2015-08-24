# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0005_show_end_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurrence',
            name='_lookup_ptr',
        ),
        migrations.AlterField(
            model_name='show',
            name='recurrence',
            field=recurrence.fields.RecurrenceField(),
        ),
        migrations.DeleteModel(
            name='_Lookup',
        ),
        migrations.DeleteModel(
            name='Recurrence',
        ),
    ]
