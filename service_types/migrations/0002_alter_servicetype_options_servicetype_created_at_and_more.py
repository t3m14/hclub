# Generated by Django 4.2.7 on 2025-07-16 10:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service_types', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicetype',
            options={'verbose_name': 'Тип услуги', 'verbose_name_plural': 'Типы услуг'},
        ),
        migrations.AddField(
            model_name='servicetype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servicetype',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='benefits',
            field=models.JSONField(blank=True, default=list, verbose_name='Преимущества'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='benefits_images',
            field=models.JSONField(blank=True, default=list, verbose_name='Изображения преимуществ'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='client_types',
            field=models.JSONField(blank=True, default=list, verbose_name='Типы клиентов'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='main_image',
            field=models.URLField(blank=True, null=True, verbose_name='Основное изображение'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='products',
            field=models.JSONField(blank=True, default=list, verbose_name='Продукты'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='URL slug'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='target',
            field=models.CharField(max_length=100, verbose_name='Цель'),
        ),
    ]
