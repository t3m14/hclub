from django.db import models
from django.contrib.postgres.fields import ArrayField


class Contact(models.Model):
    email = models.EmailField(verbose_name='Email')
    phones = ArrayField(
        models.CharField(max_length=20),
        size=5,
        blank=True,
        default=list,
        verbose_name='Телефоны'
    )
    instagram = models.URLField(blank=True, verbose_name='Instagram')
    telegram = models.URLField(blank=True, verbose_name='Telegram')
    whatsapp = models.URLField(blank=True, verbose_name='WhatsApp')
    schedule = models.JSONField(default=list, blank=True, verbose_name='Расписание')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        
    def __str__(self):
        return self.email