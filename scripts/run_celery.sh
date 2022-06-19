#!/bin/sh
su -c "celery -A tasks worker --loglevel INFO"
