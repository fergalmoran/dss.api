#!/bin/sh
su -m djworker -c "python manage.py runserver_plus 0.0.0.0:8000"
