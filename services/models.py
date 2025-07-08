from django.db import models
from django.core.validators import MinValueValidator
from slugify import slugify
from django.contrib.postgres.fields import ArrayField


class ServiceType(models.Model):
    TARGET_CHOICES = [
        ('волосы', 'Волосы'),
        ('маникюр', 'Маникюр'),
        ('макияж', 'Макияж'),
    ]
    
    CLIENT_TYPE_CHOICES = [
        ('для мужчин', 'Для мужчин'),
        ('для женщин', 'Для женщин'),
        ('для детей', 'Для детей'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    client_types = ArrayField(
        models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES),
        size=3,
        blank=True,
        default=list,
        verbose_name='Типы клиентов'
    )
    main_image = models.URLField(blank=True, null=True, verbose_name='Основное изображение')
    benefits = models.JSONField(default=list, blank=True, verbose_name='Преимущества')
    benefits_images = ArrayField(
        models.URLField(),
        size=10,
        blank=True,
        default=list,
        verbose_name='Изображения преимуществ'
    )
    target = models.CharField(max_length=20, choices=TARGET_CHOICES, verbose_name='Цель')
    products = models.ManyToManyField('products.Product', blank=True, verbose_name='Продукты')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Slug')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
    
    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        
        while ServiceType.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    service_type = models.ForeignKey(
        ServiceType, 
        on_delete=models.CASCADE, 
        related_name='services',
        verbose_name='Тип услуги'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    price_from = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name='Цена от'
    )
    price_to = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        verbose_name='Цена до'
    )
    main_images = ArrayField(
        models.URLField(),
        size=2,
        blank=True,
        default=list,
        verbose_name='Основные изображения'
    )
    duration = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name='Продолжительность (часы)'
    )
    steps = models.JSONField(default=list, blank=True, verbose_name='Этапы услуги')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Slug')
    
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
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        
        while Service.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug
    