#!/bin/sh
su -m djworker -c "celery worker -A dss.celeryconf -Q default"
chown djworker /files -R
chown djworker /tmp/dss.log