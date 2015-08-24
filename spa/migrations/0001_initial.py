# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models
from django.conf import settings
import spa.models.mix
import spa.models.venue
import spa.models.userprofile
import spa.models.release


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='_Lookup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('message', models.TextField(verbose_name='Message')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('comment', models.CharField(max_length=1024)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('time_index', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('description', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('sent_at', models.DateTimeField(null=True, auto_now=True)),
                ('read_at', models.DateTimeField(null=True, blank=True)),
                ('body', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('mix_image', models.ImageField(upload_to=spa.models.mix.mix_image_name, max_length=1024, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('waveform_generated', models.BooleanField(default=False)),
                ('waveform_version', models.IntegerField(default=1)),
                ('mp3tags_updated', models.BooleanField(default=False)),
                ('uid', models.CharField(max_length=38, unique=True, blank=True)),
                ('filetype', models.CharField(max_length=10, default='mp3')),
                ('download_allowed', models.BooleanField(default=False)),
                ('duration', models.IntegerField(null=True, blank=True)),
                ('archive_path', models.CharField(max_length=2048, null=True, blank=True)),
                ('archive_updated', models.BooleanField(default=False)),
                ('slug', models.SlugField()),
            ],
            options={
                'permissions': (('mix_add_homepage', 'Can add a mix to the homepage'), ('mix_allow_download', 'Can allow downloads on a mix')),
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('verb', models.CharField(max_length=200, null=True)),
                ('type', models.CharField(max_length=200, null=True)),
                ('target', models.CharField(max_length=200, null=True)),
                ('target_desc', models.CharField(max_length=200, null=True)),
                ('accepted_date', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('public', models.BooleanField(default=True)),
                ('slug', models.SlugField()),
                ('mixes', models.ManyToManyField(to='spa.Mix')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('url', models.URLField()),
                ('provider', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('release_artist', models.CharField(max_length=100)),
                ('release_title', models.CharField(max_length=100)),
                ('release_description', models.TextField()),
                ('release_image', models.ImageField(upload_to=spa.models.release.release_image_name, blank=True)),
                ('release_date', models.DateField(auto_now=True)),
                ('embed_code', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('release_label', models.ForeignKey(to='spa.Label')),
            ],
        ),
        migrations.CreateModel(
            name='ReleaseAudio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('description', models.TextField()),
                ('release', models.ForeignKey(related_name='release_audio', blank=True, null=True, to='spa.Release')),
            ],
        ),
        migrations.CreateModel(
            name='Tracklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('index', models.SmallIntegerField()),
                ('timeindex', models.TimeField(null=True)),
                ('description', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('remixer', models.CharField(max_length=255)),
                ('label', models.CharField(max_length=255)),
                ('mix', models.ForeignKey(related_name='tracklist', to='spa.Mix')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('avatar_type', models.CharField(max_length=15, default='social')),
                ('avatar_image', models.ImageField(upload_to=spa.models.userprofile.avatar_name, max_length=1024, blank=True)),
                ('display_name', models.CharField(max_length=35, blank=True)),
                ('description', models.CharField(max_length=2048, blank=True)),
                ('slug', models.SlugField(default=None, null=True, blank=True)),
                ('activity_sharing_networks', models.IntegerField(default=0)),
                ('activity_sharing_facebook', bitfield.models.BitField((('plays', 'Plays'), ('likes', 'Likes'), ('favourites', 'Favourites'), ('follows', 'Follows'), ('comments', 'Comments')), default=0)),
                ('activity_sharing_twitter', bitfield.models.BitField((('plays', 'Plays'), ('likes', 'Likes'), ('favourites', 'Favourites'), ('follows', 'Follows'), ('comments', 'Comments')), default=0)),
                ('email_notifications', bitfield.models.BitField((('plays', 'Plays'), ('likes', 'Likes'), ('favourites', 'Favourites'), ('follows', 'Follows'), ('comments', 'Comments')), default=0)),
                ('city', models.CharField(max_length=100, null=True, blank=True)),
                ('country', models.CharField(max_length=100, null=True, blank=True)),
                ('last_known_session', models.CharField(max_length=250, null=True, blank=True)),
                ('following', models.ManyToManyField(related_name='followers', to='spa.UserProfile', blank=True)),
                ('user', models.OneToOneField(related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('object_created', models.DateTimeField(auto_now_add=True)),
                ('object_updated', models.DateTimeField(db_index=True, auto_now=True)),
                ('venue_name', models.CharField(max_length=250)),
                ('venue_address', models.CharField(max_length=1024)),
                ('venue_image', models.ImageField(upload_to=spa.models.venue.venue_image_name, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityComment',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='spa.Activity')),
            ],
            options={
                'abstract': False,
            },
            bases=('spa.activity',),
        ),
        migrations.CreateModel(
            name='ActivityDownload',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='spa.Activity')),
            ],
            options={
                'abstract': False,
            },
            bases=('spa.activity',),
        ),
        migrations.CreateModel(
            name='ActivityFavourite',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='spa.Activity')),
            ],
            options={
                'abstract': False,
            },
            bases=('spa.activity',),
        ),
        migrations.CreateModel(
            name='ActivityFollow',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='spa.Activity')),
                ('to_user', models.ForeignKey(related_name='activity_follow', to='spa.UserProfile')),
            ],
            options={
                'abstract': False,
            },
            bases=('spa.activity',),
        ),
        migrations.CreateModel(
            name='ActivityLike',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='spa.Activity')),
            ],
            bases=('spa.activity',),
        ),
        migrations.CreateModel(
            name='ActivityPlay',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='spa.Activity')),
            ],
            options={
                'abstract': False,
            },
            bases=('spa.activity',),
        ),
        migrations.CreateModel(
            name='Recurrence',
            fields=[
                ('_lookup_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, parent_link=True, to='spa._Lookup')),
            ],
            options={
                'abstract': False,
            },
            bases=('spa._lookup',),
        ),
        migrations.AddField(
            model_name='release',
            name='user',
            field=models.ForeignKey(editable=False, to='spa.UserProfile'),
        ),
        migrations.AddField(
            model_name='purchaselink',
            name='track',
            field=models.ForeignKey(related_name='purchase_link', to='spa.Tracklist'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(related_name='playlists', to='spa.UserProfile'),
        ),
        migrations.AddField(
            model_name='notification',
            name='from_user',
            field=models.ForeignKey(related_name='notifications', blank=True, null=True, to='spa.UserProfile'),
        ),
        migrations.AddField(
            model_name='notification',
            name='to_user',
            field=models.ForeignKey(related_name='to_notications', to='spa.UserProfile'),
        ),
        migrations.AddField(
            model_name='mix',
            name='favourites',
            field=models.ManyToManyField(related_name='favourites', to='spa.UserProfile', blank=True),
        ),
        migrations.AddField(
            model_name='mix',
            name='genres',
            field=models.ManyToManyField(to='spa.Genre'),
        ),
        migrations.AddField(
            model_name='mix',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to='spa.UserProfile', blank=True),
        ),
        migrations.AddField(
            model_name='mix',
            name='user',
            field=models.ForeignKey(related_name='mixes', to='spa.UserProfile'),
        ),
        migrations.AddField(
            model_name='message',
            name='from_user',
            field=models.ForeignKey(related_name='sent_messages', blank=True, null=True, to='spa.UserProfile'),
        ),
        migrations.AddField(
            model_name='message',
            name='to_user',
            field=models.ForeignKey(related_name='messages', blank=True, null=True, to='spa.UserProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(related_name='liked_comments', to='spa.UserProfile', blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='mix',
            field=models.ForeignKey(related_name='comments', editable=False, blank=True, null=True, to='spa.Mix'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(editable=False, blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='user',
            field=models.ForeignKey(related_name='chat_messages', blank=True, null=True, to='spa.UserProfile'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(blank=True, null=True, to='spa.UserProfile'),
        ),
        migrations.AddField(
            model_name='activityplay',
            name='mix',
            field=models.ForeignKey(related_name='activity_plays', to='spa.Mix'),
        ),
        migrations.AddField(
            model_name='activitylike',
            name='mix',
            field=models.ForeignKey(related_name='activity_likes', to='spa.Mix'),
        ),
        migrations.AddField(
            model_name='activityfavourite',
            name='mix',
            field=models.ForeignKey(related_name='activity_favourites', to='spa.Mix'),
        ),
        migrations.AddField(
            model_name='activitydownload',
            name='mix',
            field=models.ForeignKey(related_name='activity_downloads', to='spa.Mix'),
        ),
        migrations.AddField(
            model_name='activitycomment',
            name='mix',
            field=models.ForeignKey(related_name='activity_comments', to='spa.Mix'),
        ),
    ]
