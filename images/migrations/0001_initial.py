# Generated by Django 4.2.7 on 2025-07-16 09:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.ImageField(upload_to='images/original/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])], verbose_name='Оригинальное изображение')),
                ('processed_image', models.ImageField(blank=True, null=True, upload_to='images/processed/', verbose_name='Обработанное изображение')),
                ('cropped_image', models.ImageField(blank=True, null=True, upload_to='images/cropped/', verbose_name='Обрезанное изображение')),
                ('is_compressed', models.BooleanField(default=True, verbose_name='Сжато')),
                ('is_cropped', models.BooleanField(default=False, verbose_name='Обрезано')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
                'ordering': ['-created_at'],
            },
        ),
    ]
