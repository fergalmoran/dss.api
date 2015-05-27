#update poorly saved descriptions
    update spa_userprofile set description = '' where description like('Just another%')

#import the avatars
    python manage.py get_avatars
    
#jiggle the waveforms
    python manage.py zoom_convert_waveforms
    
