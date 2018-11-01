# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0016_remove_show_recurrence_rrule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('date_created', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=1024)),
                ('body', models.TextField()),
                ('user', models.ForeignKey(blank=True, to='spa.UserProfile', null=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
