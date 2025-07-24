# services/models.py
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
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    price_from = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Цена от (руб.)',
        help_text='Цена в рублях'
    )
    price_to = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Цена до (руб.)',
        help_text='Цена в рублях'
    )
    main_images = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Основные изображения'
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Продолжительность',
        help_text='Например: "2 ч. 30 м." или "90 минут"'
    )
    steps = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Этапы услуги'
    )
    target = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Цель'
    )
    client_types = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Типы клиентов (массив строк)',
        help_text='Например: ["для мужчин", "для женщин", "для детей"]'
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