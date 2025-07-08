import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_salon_api.settings')

app = Celery('beauty_salon_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()