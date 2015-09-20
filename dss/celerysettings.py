from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'spa.tasks.play_pending_audio',
        'schedule': timedelta(seconds=10)
    },
}

CELERY_TIMEZONE = 'UTC'