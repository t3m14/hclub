from django.db import models
from django.utils import timezone
import random
import logging

class Quote(models.Model):
    author = models.CharField(max_length=100, blank=True, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст цитаты')
    is_used = models.BooleanField(default=False, verbose_name='Использована')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'
        
    def __str__(self):
        return f"{self.text[:50]}..."
    
    @classmethod
    def get_random_quote(cls):
        """Получение случайной цитаты с учетом ротации"""
        # Проверяем, есть ли неиспользованные цитаты
        unused_quotes = cls.objects.filter(is_used=False)
        
        if not unused_quotes.exists():
            # Если все цитаты использованы, сбрасываем флаги
            cls.objects.all().update(is_used=False)
            unused_quotes = cls.objects.all()
        
        # Выбираем случайную цитату
        if unused_quotes.exists():
            quote = unused_quotes.order_by('?').first()
            quote.is_used = True
            quote.save()
            return quote
        
        return None


class DailyQuote(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, verbose_name='Цитата')
    date = models.DateField(unique=True, verbose_name='Дата')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Цитата дня'
        verbose_name_plural = 'Цитаты дня'
        ordering = ['-date']
        
    def __str__(self):
        return f"Цитата на {self.date}"
    
    @classmethod
    def get_today_quote(cls):
        
        """Получение цитаты на сегодня"""
        today = timezone.now().date()
        logging.info(f"Получение цитаты дня для {today}")
        # Проверяем, есть ли цитата на сегодня
        daily_quote = cls.objects.filter(date=today).first()
        
        if not daily_quote:
            # Получаем новую случайную цитату
            random_quote = Quote.get_random_quote()
            if random_quote:
                daily_quote = cls.objects.create(
                    quote=random_quote,
                    date=today
                )
        
        return daily_quote