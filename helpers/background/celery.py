import os
from celery import Celery

os.environ.setdefault('CELERY_CONFIG_MODULE', 'helpers.background.celeryconfig')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


app = Celery('Exam')

app.config_from_envvar('CELERY_CONFIG_MODULE')
