#!/bin/sh

/app/wait.sh  -t 20 -h "$POSTGRESQL_HOST" -p "$POSTGRESQL_PORT"
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input

exec "$@"