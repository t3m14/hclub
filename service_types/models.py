from django.db import models
from slugify import slugify


class ServiceType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    client_types = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Типы клиентов'
    )
    main_image = models.URLField(
        blank=True, 
        null=True,
        verbose_name='Основное изображение'
    )
    benefits = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Преимущества'
    )
    benefits_images = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Изображения преимуществ'
    )
    target = models.CharField(
        max_length=200,
        verbose_name='Цель'
    )
    products = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Продукты'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL slug'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Генерируем slug при создании или если название изменилось
        if not self.pk or self._state.adding or 'name' in getattr(self, '_changed_fields', []):
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
    
    def generate_unique_slug(self):
        """Генерация уникального slug"""
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        
        while ServiceType.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        return slug