from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image
import os
from django.conf import settings


class ImageUpload(models.Model):
    original_image = models.ImageField(
        upload_to='images/original/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        verbose_name='Оригинальное изображение'
    )
    processed_image = models.ImageField(
        upload_to='images/processed/',
        blank=True,
        null=True,
        verbose_name='Обработанное изображение'
    )
    cropped_image = models.ImageField(
        upload_to='images/cropped/',
        blank=True,
        null=True,
        verbose_name='Обрезанное изображение'
    )
    is_compressed = models.BooleanField(default=True, verbose_name='Сжато')
    is_cropped = models.BooleanField(default=False, verbose_name='Обрезано')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Изображение {self.id}"
    
    def save(self, *args, **kwargs):
        # Сначала сохраняем объект
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Обрабатываем изображение только для новых объектов
        if is_new and self.original_image:
            self.process_image()
    
    def process_image(self):
        """Обработка изображения: конвертация в webp, сжатие, обрезка"""
        try:
            image_path = self.original_image.path
            
            with Image.open(image_path) as img:
                # Конвертация в RGB если нужно
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Сжатие изображения
                if self.is_compressed:
                    # Изменение размера если изображение слишком большое
                    max_size = (1920, 1080)
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Сохранение обработанного изображения в webp
                    processed_path = self.get_processed_path()
                    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
                    img.save(processed_path, 'WEBP', quality=85, optimize=True)
                    
                    # Обновление поля processed_image
                    processed_relative_path = os.path.relpath(processed_path, settings.MEDIA_ROOT)
                    self.processed_image.name = processed_relative_path
                
                # Обрезка изображения
                if self.is_cropped:
                    # Обрезка до 600px (квадрат)
                    size = (600, 600)
                    img_cropped = img.copy()
                    img_cropped.thumbnail(size, Image.Resampling.LANCZOS)
                    
                    # Создание квадратного изображения
                    img_square = Image.new('RGB', size, (255, 255, 255))
                    img_square.paste(
                        img_cropped,
                        ((size[0] - img_cropped.size[0]) // 2,
                         (size[1] - img_cropped.size[1]) // 2)
                    )
                    
                    # Сохранение обрезанного изображения
                    cropped_path = self.get_cropped_path()
                    os.makedirs(os.path.dirname(cropped_path), exist_ok=True)
                    img_square.save(cropped_path, 'WEBP', quality=85, optimize=True)
                    
                    # Обновление поля cropped_image
                    cropped_relative_path = os.path.relpath(cropped_path, settings.MEDIA_ROOT)
                    self.cropped_image.name = cropped_relative_path
            
            # Сохранение обновленных полей
            ImageUpload.objects.filter(id=self.id).update(
                processed_image=self.processed_image.name if self.processed_image else None,
                cropped_image=self.cropped_image.name if self.cropped_image else None
            )
            
        except Exception as e:
            print(f"Ошибка обработки изображения: {e}")
    
    def get_processed_path(self):
        """Генерация пути для обработанного изображения"""
        base_name = os.path.splitext(os.path.basename(self.original_image.name))[0]
        return os.path.join(settings.MEDIA_ROOT, 'images', 'processed', f'{base_name}_processed.webp')
    
    def get_cropped_path(self):
        """Генерация пути для обрезанного изображения"""
        base_name = os.path.splitext(os.path.basename(self.original_image.name))[0]
        return os.path.join(settings.MEDIA_ROOT, 'images', 'cropped', f'{base_name}_cropped.webp')
    
    def get_image_url(self):
        """Получение URL изображения (приоритет: обработанное -> оригинальное)"""
        if self.processed_image:
            return self.processed_image.url
        if self.original_image:
            return self.original_image.url
        return None
    
    def get_cropped_url(self):
        """Получение URL обрезанного изображения"""
        if self.cropped_image:
            return self.cropped_image.url
        return self.get_image_url()