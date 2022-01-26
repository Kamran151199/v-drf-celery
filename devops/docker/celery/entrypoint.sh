#!/bin/sh

/app/wait.sh  -t 20 -h "$POSTGRESQL_HOST" -p "$POSTGRESQL_PORT"

exec "$@"