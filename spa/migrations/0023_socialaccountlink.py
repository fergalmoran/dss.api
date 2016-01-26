# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('spa', '0022_auto_20151112_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAccountLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('type', models.CharField(max_length=30, choices=[('twitter', 'Twitter'), ('facebook', 'Facebook'),
                                                                  ('google', 'Google')])),
                ('social_id', models.CharField(max_length=150)),
                ('user', models.ForeignKey(to='spa.UserProfile', related_name='social_accounts')),
            ],
            options={
                'abstract': False,
            },
        )
    ]
