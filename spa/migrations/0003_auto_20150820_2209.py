# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0002_show'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='show',
            name='test_field',
        ),
        migrations.AddField(
            model_name='show',
            name='user',
            field=models.ForeignKey(default=2, related_name='show', to='spa.UserProfile'),
            preserve_default=False,
        ),
    ]
