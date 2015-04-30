# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('spa_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('avatar_type', self.gf('django.db.models.fields.CharField')(default='social', max_length=15)),
            ('avatar_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(default=None, max_length=35, null=True, blank=True)),
            ('activity_sharing', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('activity_sharing_networks', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('spa', ['UserProfile'])

        # Adding model 'ChatMessage'
        db.create_table('spa_chatmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='chat_messages', null=True, to=orm['spa.UserProfile'])),
        ))
        db.send_create_signal('spa', ['ChatMessage'])

        # Adding model '_Lookup'
        db.create_table('spa__lookup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('spa', ['_Lookup'])

        # Adding model 'Recurrence'
        db.create_table('spa_recurrence', (
            ('_lookup_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spa._Lookup'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('spa', ['Recurrence'])

        # Adding model 'Genre'
        db.create_table('spa_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('spa', ['Genre'])

        # Adding model '_Activity'
        db.create_table('spa__activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('spa', ['_Activity'])

        # Adding model 'MixPlay'
        db.create_table('spa_mixplay', (
            ('_activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spa._Activity'], unique=True, primary_key=True)),
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='plays', to=orm['spa.Mix'])),
        ))
        db.send_create_signal('spa', ['MixPlay'])

        # Adding model 'MixDownload'
        db.create_table('spa_mixdownload', (
            ('_activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spa._Activity'], unique=True, primary_key=True)),
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='downloads', to=orm['spa.Mix'])),
        ))
        db.send_create_signal('spa', ['MixDownload'])

        # Adding model 'Mix'
        db.create_table('spa_mix', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 12, 0, 0))),
            ('mix_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('local_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('download_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('stream_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spa.UserProfile'])),
            ('waveform_generated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=38, blank=True)),
            ('download_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('spa', ['Mix'])

        # Adding M2M table for field genres on 'Mix'
        db.create_table('spa_mix_genres', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mix', models.ForeignKey(orm['spa.mix'], null=False)),
            ('genre', models.ForeignKey(orm['spa.genre'], null=False))
        ))
        db.create_unique('spa_mix_genres', ['mix_id', 'genre_id'])

        # Adding model 'Comment'
        db.create_table('spa_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='comments', null=True, to=orm['spa.Mix'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('time_index', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('spa', ['Comment'])

        # Adding model 'Venue'
        db.create_table('spa_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('venue_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('venue_address', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('venue_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('spa', ['Venue'])

        # Adding model 'Event'
        db.create_table('spa_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spa.Venue'])),
            ('event_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 12, 0, 0))),
            ('event_time', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 3, 12, 0, 0))),
            ('date_created', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 12, 0, 0))),
            ('event_title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('event_description', self.gf('tinymce.views.HTMLField')()),
            ('event_recurrence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spa.Recurrence'])),
        ))
        db.send_create_signal('spa', ['Event'])

        # Adding M2M table for field attendees on 'Event'
        db.create_table('spa_event_attendees', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['spa.event'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('spa_event_attendees', ['event_id', 'user_id'])

        # Adding model 'Label'
        db.create_table('spa_label', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('spa', ['Label'])

        # Adding model 'MixLike'
        db.create_table('spa_mixlike', (
            ('_activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spa._Activity'], unique=True, primary_key=True)),
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='likes', to=orm['spa.Mix'])),
        ))
        db.send_create_signal('spa', ['MixLike'])

        # Adding model 'MixFavourite'
        db.create_table('spa_mixfavourite', (
            ('_activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spa._Activity'], unique=True, primary_key=True)),
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='favourites', to=orm['spa.Mix'])),
        ))
        db.send_create_signal('spa', ['MixFavourite'])

        # Adding model 'Tracklist'
        db.create_table('spa_tracklist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tracklist', to=orm['spa.Mix'])),
            ('index', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('timeindex', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('remixer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('spa', ['Tracklist'])

        # Adding model 'PurchaseLink'
        db.create_table('spa_purchaselink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchase_link', to=orm['spa.Tracklist'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('spa', ['PurchaseLink'])

        # Adding model 'Release'
        db.create_table('spa_release', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('release_artist', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('release_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('release_description', self.gf('django.db.models.fields.TextField')()),
            ('release_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('release_label', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spa.Label'])),
            ('release_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 12, 0, 0))),
            ('embed_code', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spa.UserProfile'])),
        ))
        db.send_create_signal('spa', ['Release'])

        # Adding model 'ReleaseAudio'
        db.create_table('spa_releaseaudio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('local_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='release_audio', null=True, to=orm['spa.Release'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('spa', ['ReleaseAudio'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('spa_userprofile')

        # Deleting model 'ChatMessage'
        db.delete_table('spa_chatmessage')

        # Deleting model '_Lookup'
        db.delete_table('spa__lookup')

        # Deleting model 'Recurrence'
        db.delete_table('spa_recurrence')

        # Deleting model 'Genre'
        db.delete_table('spa_genre')

        # Deleting model '_Activity'
        db.delete_table('spa__activity')

        # Deleting model 'MixPlay'
        db.delete_table('spa_mixplay')

        # Deleting model 'MixDownload'
        db.delete_table('spa_mixdownload')

        # Deleting model 'Mix'
        db.delete_table('spa_mix')

        # Removing M2M table for field genres on 'Mix'
        db.delete_table('spa_mix_genres')

        # Deleting model 'Comment'
        db.delete_table('spa_comment')

        # Deleting model 'Venue'
        db.delete_table('spa_venue')

        # Deleting model 'Event'
        db.delete_table('spa_event')

        # Removing M2M table for field attendees on 'Event'
        db.delete_table('spa_event_attendees')

        # Deleting model 'Label'
        db.delete_table('spa_label')

        # Deleting model 'MixLike'
        db.delete_table('spa_mixlike')

        # Deleting model 'MixFavourite'
        db.delete_table('spa_mixfavourite')

        # Deleting model 'Tracklist'
        db.delete_table('spa_tracklist')

        # Deleting model 'PurchaseLink'
        db.delete_table('spa_purchaselink')

        # Deleting model 'Release'
        db.delete_table('spa_release')

        # Deleting model 'ReleaseAudio'
        db.delete_table('spa_releaseaudio')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'spa._activity': {
            'Meta': {'object_name': '_Activity'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'spa._lookup': {
            'Meta': {'object_name': '_Lookup'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spa.chatmessage': {
            'Meta': {'object_name': 'ChatMessage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'chat_messages'", 'null': 'True', 'to': "orm['spa.UserProfile']"})
        },
        'spa.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comments'", 'null': 'True', 'to': "orm['spa.Mix']"}),
            'time_index': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'spa.event': {
            'Meta': {'object_name': 'Event'},
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'attendees'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 12, 0, 0)'}),
            'event_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 12, 0, 0)'}),
            'event_description': ('tinymce.views.HTMLField', [], {}),
            'event_recurrence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.Recurrence']"}),
            'event_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 3, 12, 0, 0)'}),
            'event_title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'event_venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.Venue']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spa.genre': {
            'Meta': {'object_name': 'Genre'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'spa.label': {
            'Meta': {'object_name': 'Label'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'spa.mix': {
            'Meta': {'object_name': 'Mix'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'download_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'download_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['spa.Genre']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'local_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'mix_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'stream_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '38', 'blank': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 12, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.UserProfile']"}),
            'waveform_generated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'spa.mixdownload': {
            'Meta': {'object_name': 'MixDownload', '_ormbases': ['spa._Activity']},
            '_activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa._Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'downloads'", 'to': "orm['spa.Mix']"})
        },
        'spa.mixfavourite': {
            'Meta': {'object_name': 'MixFavourite', '_ormbases': ['spa._Activity']},
            '_activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa._Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'favourites'", 'to': "orm['spa.Mix']"})
        },
        'spa.mixlike': {
            'Meta': {'object_name': 'MixLike', '_ormbases': ['spa._Activity']},
            '_activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa._Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'likes'", 'to': "orm['spa.Mix']"})
        },
        'spa.mixplay': {
            'Meta': {'object_name': 'MixPlay', '_ormbases': ['spa._Activity']},
            '_activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa._Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'plays'", 'to': "orm['spa.Mix']"})
        },
        'spa.purchaselink': {
            'Meta': {'object_name': 'PurchaseLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_link'", 'to': "orm['spa.Tracklist']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'spa.recurrence': {
            'Meta': {'object_name': 'Recurrence', '_ormbases': ['spa._Lookup']},
            '_lookup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa._Lookup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'spa.release': {
            'Meta': {'object_name': 'Release'},
            'embed_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'release_artist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'release_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 12, 0, 0)'}),
            'release_description': ('django.db.models.fields.TextField', [], {}),
            'release_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'release_label': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.Label']"}),
            'release_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.UserProfile']"})
        },
        'spa.releaseaudio': {
            'Meta': {'object_name': 'ReleaseAudio'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_audio'", 'null': 'True', 'to': "orm['spa.Release']"})
        },
        'spa.tracklist': {
            'Meta': {'object_name': 'Tracklist'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.SmallIntegerField', [], {}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tracklist'", 'to': "orm['spa.Mix']"}),
            'remixer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timeindex': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'spa.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activity_sharing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'activity_sharing_networks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avatar_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'avatar_type': ('django.db.models.fields.CharField', [], {'default': "'social'", 'max_length': '15'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'spa.venue': {
            'Meta': {'object_name': 'Venue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'venue_address': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'venue_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'venue_name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['spa']