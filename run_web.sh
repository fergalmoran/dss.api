#!/bin/bash
python manage.py migrate

chmod 777 /files/tmp/dss.log

touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

echo "Starting gunicorn"
exec gunicorn dss.wsgi:application \
         --bind 0.0.0.0:8001
         --workers 4 \
         --log-level=info \
         --log-file=/srv/logs/gunicorn.log \
         --access-logfile=/srv/logs/access.log \
         "$@"
