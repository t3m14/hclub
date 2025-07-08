# beauty_salon_api/celery.py
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_salon_api.settings')

app = Celery('beauty_salon_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# beauty_salon_api/__init__.py
from .celery import app as celery_app

__all__ = ('celery_app',)


# quotes/tasks.py
from celery import shared_task
from .models import DailyQuote
from django.utils import timezone


@shared_task
def update_daily_quote():
    """Задача для обновления цитаты дня"""
    today = timezone.now().date()
    
    # Получаем цитату на сегодня (создастся автоматически если её нет)
    daily_quote = DailyQuote.get_today_quote()
    
    if daily_quote:
        return f"Цитата дня обновлена на {today}: {daily_quote.quote.text[:50]}..."
    
    return f"Не удалось обновить цитату на {today}"


# Добавить в settings.py:
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'

# Периодические задачи
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'update-daily-quote': {
        'task': 'quotes.tasks.update_daily_quote',
        'schedule': crontab(hour=0, minute=0),  # Каждый день в полночь
    },
}


# Для запуска:
# celery -A beauty_salon_api worker -l info
# celery -A beauty_salon_api beat -l info