
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