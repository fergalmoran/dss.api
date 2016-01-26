# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0023_socialaccountlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialaccountlink',
            name='access_token',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='socialaccountlink',
            name='access_token_secret',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
