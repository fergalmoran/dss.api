#!/bin/sh
su -m djworker -c "sleep 3 && celery worker -A dss.celeryconf -Q default"
