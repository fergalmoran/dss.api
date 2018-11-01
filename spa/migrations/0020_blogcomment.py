# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0019_blog_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('comment', models.CharField(max_length=1024)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('blog', models.ForeignKey(to='spa.Blog', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(null=True, to='spa.UserProfile', blank=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
