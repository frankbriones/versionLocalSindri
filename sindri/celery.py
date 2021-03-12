import os
from celery import Celery
from django.conf import settings

# Setear variable de entorno
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sindri.settings")

app = Celery('sindri',
             broker='amqp://celery_user:celery@localhost:5672/celery_host',
             )

app.config_from_object("django.conf:settings", namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
