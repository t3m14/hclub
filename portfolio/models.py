from django.db import models


class Portfolio(models.Model):
    image = models.URLField(verbose_name='Изображение')
    master = models.JSONField(verbose_name='Мастер')  # Хранится как объект, не привязан к ID
    service_type = models.ForeignKey(
        'services.ServiceType',
        on_delete=models.CASCADE,
        related_name='portfolio_items',
        verbose_name='Тип услуги'
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='portfolio_items',
        verbose_name='Услуга'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'
        
    def __str__(self):
        master_name = self.master.get('name', 'Неизвестный мастер') if isinstance(self.master, dict) else str(self.master)
        return f"Работа {master_name} - {self.service_type.name}"