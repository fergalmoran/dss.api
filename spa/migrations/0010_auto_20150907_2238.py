# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0009_auto_20150821_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='end_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='mix',
            field=models.ForeignKey(null=True, related_name='show', to='spa.Mix', blank=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='show',
            name='recurrence',
            field=recurrence.fields.RecurrenceField(blank=True),
        ),
    ]
