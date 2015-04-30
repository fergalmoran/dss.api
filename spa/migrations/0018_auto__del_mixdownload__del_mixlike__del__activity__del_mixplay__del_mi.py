# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MixDownload'
        #db.delete_table(u'spa_activity')
        #db.delete_table(u'spa_activitymix')
        #db.delete_table(u'spa_mixdownload')

        # Deleting model 'MixLike'
        db.delete_table(u'spa_mixlike')

        # Deleting model '_Activity'
        db.delete_table(u'spa__activity')

        # Deleting model 'MixPlay'
        db.delete_table(u'spa_mixplay')

        # Deleting model 'MixFavourite'
        db.delete_table(u'spa_mixfavourite')

        # Adding model 'Activity'
        db.create_table(u'spa_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spa.UserProfile'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('spa', ['Activity'])

        # Adding model 'ActivityMix'
        db.create_table(u'spa_activitymix', (
            (u'activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spa.Activity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('spa', ['ActivityMix'])


    def backwards(self, orm):
        # Adding model 'MixDownload'
        db.create_table(u'spa_mixdownload', (
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='downloads', to=orm['spa.Mix'])),
            (u'_activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spa._Activity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('spa', ['MixDownload'])

        # Adding model 'MixLike'
        db.create_table(u'spa_mixlike', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='likes', to=orm['spa.Mix'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='likes', to=orm['auth.User'])),
        ))
        db.send_create_signal('spa', ['MixLike'])

        # Adding model '_Activity'
        db.create_table(u'spa__activity', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activity', null=True, to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('spa', ['_Activity'])

        # Adding model 'MixPlay'
        db.create_table(u'spa_mixplay', (
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='plays', to=orm['spa.Mix'])),
            (u'_activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spa._Activity'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('spa', ['MixPlay'])

        # Adding model 'MixFavourite'
        db.create_table(u'spa_mixfavourite', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('mix', self.gf('django.db.models.fields.related.ForeignKey')(related_name='favourites', to=orm['spa.Mix'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='favourites', to=orm['auth.User'])),
        ))
        db.send_create_signal('spa', ['MixFavourite'])

        # Deleting model 'Activity'
        db.delete_table(u'spa_activity')

        # Deleting model 'ActivityMix'
        db.delete_table(u'spa_activitymix')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'spa._lookup': {
            'Meta': {'object_name': '_Lookup'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spa.activity': {
            'Meta': {'object_name': 'Activity'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        'spa.activitymix': {
            'Meta': {'object_name': 'ActivityMix', '_ormbases': ['spa.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa.Activity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'spa.chatmessage': {
            'Meta': {'object_name': 'ChatMessage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'chat_messages'", 'null': 'True', 'to': "orm['spa.UserProfile']"})
        },
        'spa.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comments'", 'null': 'True', 'to': "orm['spa.Mix']"}),
            'time_index': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'spa.event': {
            'Meta': {'object_name': 'Event'},
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'attendees'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 6, 8, 0, 0)'}),
            'event_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 6, 8, 0, 0)'}),
            'event_description': ('tinymce.views.HTMLField', [], {}),
            'event_recurrence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.Recurrence']"}),
            'event_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 6, 8, 0, 0)'}),
            'event_title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'event_venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.Venue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spa.genre': {
            'Meta': {'object_name': 'Genre'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'spa.label': {
            'Meta': {'object_name': 'Label'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'spa.mix': {
            'Meta': {'object_name': 'Mix'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'download_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'download_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['spa.Genre']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'local_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'mix_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'stream_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '38', 'blank': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 8, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.UserProfile']"}),
            'waveform_generated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'spa.purchaselink': {
            'Meta': {'object_name': 'PurchaseLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_link'", 'to': "orm['spa.Tracklist']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'spa.recurrence': {
            'Meta': {'object_name': 'Recurrence', '_ormbases': ['spa._Lookup']},
            u'_lookup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa._Lookup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'spa.release': {
            'Meta': {'object_name': 'Release'},
            'embed_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'release_artist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'release_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 6, 8, 0, 0)'}),
            'release_description': ('django.db.models.fields.TextField', [], {}),
            'release_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'release_label': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.Label']"}),
            'release_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.UserProfile']"})
        },
        'spa.releaseaudio': {
            'Meta': {'object_name': 'ReleaseAudio'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_audio'", 'null': 'True', 'to': "orm['spa.Release']"})
        },
        'spa.tracklist': {
            'Meta': {'object_name': 'Tracklist'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'followers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'followers_rel_+'", 'null': 'True', 'to': "orm['spa.UserProfile']"}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'following_rel_+'", 'null': 'True', 'to': "orm['spa.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'userprofile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        'spa.venue': {
            'Meta': {'object_name': 'Venue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'venue_address': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'venue_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'venue_name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['spa']
