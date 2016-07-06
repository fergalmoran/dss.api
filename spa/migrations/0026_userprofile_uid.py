# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0025_socialaccountlink_provider_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='uid',
            field=models.UUIDField(editable=False, null=True),
        ),
    ]
