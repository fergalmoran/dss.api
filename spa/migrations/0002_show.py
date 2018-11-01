# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('test_field', models.CharField(max_length=400)),
                ('mix', models.ForeignKey(related_name='show', to='spa.Mix', on_delete=models.CASCADE)),
            ],
        ),
    ]
