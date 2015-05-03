#update comments user_id to be userprofile_id
    UPDATE spa_comment SET user_id = spa_userprofile.id FROM spa_userprofile WHERE spa_comment.user_id = spa_userprofile.user_id


#import the avatars
    python manage.py get_avatars
    
#jiggle the waveforms
    python manage.py zoom_convert_waveforms