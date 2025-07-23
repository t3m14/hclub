from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image
import os
import uuid
from django.conf import settings
from django.utils.text import slugify
import logging

logger = logging.getLogger(__name__)


def upload_to_original(instance, filename):
    """Генерация безопасного пути для оригинального файла"""
    ext = filename.split('.')[-1].lower() if '.' in filename else 'jpg'
    # Берем только первые 50 символов названия файла и делаем slug
    name_part = slugify(filename.split('.')[0][:50]) or 'image'
    # Добавляем уникальный идентификатор
    unique_id = uuid.uuid4().hex[:8]
    new_filename = f"{unique_id}_{name_part}.{ext}"
    return f'images/original/{new_filename}'


def upload_to_processed(instance, filename):
    """Генерация безопасного пути для обработанного файла"""
    ext = 'webp'  # Всегда конвертируем в webp
    unique_id = uuid.uuid4().hex[:8]
    new_filename = f"{unique_id}_processed.{ext}"
    return f'images/processed/{new_filename}'


def upload_to_cropped(instance, filename):
    """Генерация безопасного пути для обрезанного файла"""
    ext = 'webp'  # Всегда конвертируем в webp
    unique_id = uuid.uuid4().hex[:8]
    new_filename = f"{unique_id}_cropped.{ext}"
    return f'images/cropped/{new_filename}'


class ImageUpload(models.Model):
    original_image = models.ImageField(
        upload_to=upload_to_original,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp', 'tiff'])],  # Добавлены форматы
        verbose_name='Оригинальное изображение'
    )
    processed_image = models.ImageField(
        upload_to=upload_to_processed,
        blank=True,
        null=True,
        verbose_name='Обработанное изображение'
    )
    cropped_image = models.ImageField(
        upload_to=upload_to_cropped,
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
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.original_image:
            try:
                self.process_image()
            except Exception as e:
                logger.error(f"Error processing image {self.id}: {str(e)}")
    
    def process_image(self):
        """Обработка изображения: конвертация в webp, сжатие, обрезка"""
        try:
            if not self.original_image:
                return
                
            image_path = self.original_image.path
            
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return
            
            with Image.open(image_path) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                if self.is_compressed:
                    max_size = (1920, 1080)
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    processed_path = self.get_processed_path()
                    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
                    img.save(processed_path, 'WEBP', quality=85, optimize=True)
                    
                    processed_relative_path = os.path.relpath(processed_path, settings.MEDIA_ROOT)
                    self.processed_image.name = processed_relative_path
                
                if self.is_cropped:
                    size = (600, 600)
                    img_cropped = img.copy()
                    img_cropped.thumbnail(size, Image.Resampling.LANCZOS)
                    
                    img_square = Image.new('RGB', size, (255, 255, 255))
                    img_square.paste(
                        img_cropped,
                        ((size[0] - img_cropped.size[0]) // 2,
                         (size[1] - img_cropped.size[1]) // 2)
                    )
                    
                    cropped_path = self.get_cropped_path()
                    os.makedirs(os.path.dirname(cropped_path), exist_ok=True)
                    img_square.save(cropped_path, 'WEBP', quality=85, optimize=True)
                    
                    cropped_relative_path = os.path.relpath(cropped_path, settings.MEDIA_ROOT)
                    self.cropped_image.name = cropped_relative_path
            
            ImageUpload.objects.filter(id=self.id).update(
                processed_image=self.processed_image.name if self.processed_image else None,
                cropped_image=self.cropped_image.name if self.cropped_image else None
            )
            
        except Exception as e:
            logger.error(f"Error processing image {self.id}: {str(e)}")
            raise
    
    def get_processed_path(self):
        """Генерация пути для обработанного изображения"""
        unique_id = uuid.uuid4().hex[:8]
        return os.path.join(settings.MEDIA_ROOT, 'images', 'processed', f'{unique_id}_processed.webp')
    
    def get_cropped_path(self):
        """Генерация пути для обрезанного изображения"""
        unique_id = uuid.uuid4().hex[:8]
        return os.path.join(settings.MEDIA_ROOT, 'images', 'cropped', f'{unique_id}_cropped.webp')
    
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