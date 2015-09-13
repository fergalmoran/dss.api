# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0014_show_recurrence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='recurrence',
            field=models.CharField(max_length=1),
        ),
    ]
