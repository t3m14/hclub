from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'brand', 'name', 'image', 'purpose',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка продуктов"""
    class Meta:
        model = Product
        fields = ['id', 'brand', 'name', 'purpose']