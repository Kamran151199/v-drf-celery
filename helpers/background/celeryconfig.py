import os

include = ['apps.users.tasks.email', 'apps.computer.tasks.pearson']  # Task modules
imports = ['apps.users.tasks.email', 'apps.computer.tasks.pearson']

enable_utc = os.environ.get('CELERY_ENABLE_UTC', True)
timezone = os.environ.get('CELERY_TIMEZONE', 'Europe/Berlin')

CELERY_BROKER_URL = f"amqp://{os.environ.get('RABBITMQ_DEFAULT_USER')}:" \
                    f"{os.environ.get('RABBITMQ_DEFAULT_PASS')}@" \
                    f"{os.environ.get('RABBITMQ_DEFAULT_HOST')}:" \
                    f"{os.environ.get('RABBITMQ_DEFAULT_PORT')}"
broker_write_url = CELERY_BROKER_URL
broker_read_url = CELERY_BROKER_URL  # TODO: // Change later
broker_connection_max_retries = int(os.environ.get('CELERY_BROKER_CONNECTION_MAX_RETRIES', 100))

result_backend = os.environ.get('CELERY_RESULT_BACKEND_URL', 'redis://username:password@host:port/db')
