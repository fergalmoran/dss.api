# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserProfile.activity_sharing'
        db.delete_column(u'spa_userprofile', 'activity_sharing')

        # Adding field 'UserProfile.activity_sharing_facebook'
        db.add_column(u'spa_userprofile', 'activity_sharing_facebook',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserProfile.activity_sharing_twitter'
        db.add_column(u'spa_userprofile', 'activity_sharing_twitter',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'UserProfile.activity_sharing'
        db.add_column(u'spa_userprofile', 'activity_sharing',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'UserProfile.activity_sharing_facebook'
        db.delete_column(u'spa_userprofile', 'activity_sharing_facebook')

        # Deleting field 'UserProfile.activity_sharing_twitter'
        db.delete_column(u'spa_userprofile', 'activity_sharing_twitter')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'schedule.calendar': {
            'Meta': {'object_name': 'Calendar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        },
        'schedule.event': {
            'Meta': {'object_name': 'Event'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Calendar']", 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'end_recurring_period': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Rule']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'schedule.rule': {
            'Meta': {'object_name': 'Rule'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'spa._lookup': {
            'Meta': {'object_name': '_Lookup'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'spa.activity': {
            'Meta': {'object_name': 'Activity'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spa.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        'spa.activitycomment': {
            'Meta': {'object_name': 'ActivityComment', '_ormbases': ['spa.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity_comments'", 'to': "orm['spa.Mix']"})
        },
        'spa.activitydownload': {
            'Meta': {'object_name': 'ActivityDownload', '_ormbases': ['spa.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity_downloads'", 'to': "orm['spa.Mix']"})
        },
        'spa.activityfavourite': {
            'Meta': {'object_name': 'ActivityFavourite', '_ormbases': ['spa.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity_favourites'", 'to': "orm['spa.Mix']"})
        },
        'spa.activityfollow': {
            'Meta': {'object_name': 'ActivityFollow', '_ormbases': ['spa.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity_follow'", 'to': "orm['spa.UserProfile']"})
        },
        'spa.activitylike': {
            'Meta': {'object_name': 'ActivityLike', '_ormbases': ['spa.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity_likes'", 'to': "orm['spa.Mix']"})
        },
        'spa.activityplay': {
            'Meta': {'object_name': 'ActivityPlay', '_ormbases': ['spa.Activity']},
            u'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spa.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity_plays'", 'to': "orm['spa.Mix']"})
        },
        'spa.chatmessage': {
            'Meta': {'object_name': 'ChatMessage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'chat_messages'", 'null': 'True', 'to': "orm['spa.UserProfile']"})
        },
        'spa.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'liked_comments'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['spa.UserProfile']"}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comments'", 'null': 'True', 'to': "orm['spa.Mix']"}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'time_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'spa.genre': {
            'Meta': {'object_name': 'Genre'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'spa.label': {
            'Meta': {'object_name': 'Label'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'spa.mix': {
            'Meta': {'object_name': 'Mix'},
            'archive_path': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'archive_updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'download_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'favourites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'favourites'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['spa.UserProfile']"}),
            'filetype': ('django.db.models.fields.CharField', [], {'default': "'mp3'", 'max_length': '10'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['spa.Genre']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'likes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['spa.UserProfile']"}),
            'mix_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'blank': 'True'}),
            'mp3tags_updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '38', 'blank': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mixes'", 'to': "orm['spa.UserProfile']"}),
            'waveform_generated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'spa.notification': {
            'Meta': {'object_name': 'Notification'},
            'accepted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'notifications'", 'null': 'True', 'to': "orm['spa.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_html': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'notification_text': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'notification_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_notications'", 'to': "orm['spa.UserProfile']"}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        'spa.playlist': {
            'Meta': {'object_name': 'Playlist'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mixes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['spa.Mix']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'playlists'", 'to': "orm['spa.UserProfile']"})
        },
        'spa.purchaselink': {
            'Meta': {'object_name': 'PurchaseLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
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
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'release_artist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'release_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)'}),
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
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_audio'", 'null': 'True', 'to': "orm['spa.Release']"})
        },
        'spa.show': {
            'Meta': {'object_name': 'Show', '_ormbases': ['schedule.Event']},
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['schedule.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'show'", 'to': "orm['spa.Mix']"})
        },
        'spa.tracklist': {
            'Meta': {'object_name': 'Tracklist'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.SmallIntegerField', [], {}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mix': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tracklist'", 'to': "orm['spa.Mix']"}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'remixer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timeindex': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'spa.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activity_sharing_facebook': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'activity_sharing_networks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'activity_sharing_twitter': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'avatar_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'blank': 'True'}),
            'avatar_type': ('django.db.models.fields.CharField', [], {'default': "'social'", 'max_length': '15'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'email_notifications': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'followers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['spa.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_known_session': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'userprofile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        'spa.venue': {
            'Meta': {'object_name': 'Venue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'object_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 2, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'venue_address': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'venue_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'venue_name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['spa']