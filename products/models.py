from django.db import models


class Product(models.Model):
    brand = models.CharField(max_length=200, verbose_name='Бренд')
    name = models.CharField(max_length=200, verbose_name='Название')
    image = models.URLField(blank=True, null=True, verbose_name='Изображение')
    purpose = models.CharField(max_length=300, verbose_name='Предназначение')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        
    def __str__(self):
        return f"{self.brand} - {self.name}"