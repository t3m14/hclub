from django.db import models
from django.core.validators import MinValueValidator


class Master(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    image = models.URLField(blank=True, null=True, verbose_name='Изображение')
    job_title = models.CharField(max_length=200, verbose_name='Должность')
    favorite_product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='favorite_masters',
        verbose_name='Любимый продукт'
    )
    service_types = models.ManyToManyField(
        'service_types.ServiceType',  # Исправлено: было 'services.ServiceType'
        related_name='masters',
        verbose_name='Типы услуг'
    )
    experience = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Опыт работы (лет)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'
        
    def __str__(self):
        return self.name