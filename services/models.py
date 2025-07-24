from django.db import models
from slugify import slugify


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    service_type = models.ForeignKey(
        'service_types.ServiceType',
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Тип услуги'
    )
    description = models.TextField(verbose_name='Описание', default='')  # Временный default
    price_from = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Цена от'
    )
    price_to = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Цена до'
    )
    main_images = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Основные изображения'
    )
    duration = models.CharField(
        max_length=50,
        verbose_name='Продолжительность',
        default='1 час'  # Временный default
    )
    steps = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Этапы услуги'
    )
    target = models.CharField(
        max_length=100,
        blank=True,
        default='',  # Временный default
        verbose_name='Цель'
    )
    client_types = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Типы клиентов (массив ID)'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL slug'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
    
    def generate_unique_slug(self):
        """Генерация уникального slug"""
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        
        while Service.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        return slug