#!/bin/sh
su -m djworker -c "python manage.py celeryd"