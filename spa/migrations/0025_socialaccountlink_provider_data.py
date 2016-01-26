# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0024_auto_20160121_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialaccountlink',
            name='provider_data',
            field=models.CharField(blank=True, null=True, max_length=2000),
        ),
    ]
