# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0010_auto_20150907_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='performer',
            field=models.ForeignKey(related_name='shows', default=2, to='spa.UserProfile', on_delete=models.CASCADE),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='show',
            name='user',
            field=models.ForeignKey(related_name='owned_shows', to='spa.UserProfile', on_delete=models.CASCADE),
        ),
    ]
