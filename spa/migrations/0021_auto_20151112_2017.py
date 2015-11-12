# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0020_blogcomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mix',
            name='download_allowed',
        ),
        migrations.AddField(
            model_name='mix',
            name='is_downloadable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mix',
            name='is_private',
            field=models.BooleanField(default=True),
        ),
    ]
