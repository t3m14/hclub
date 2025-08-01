from rest_framework import serializers
from .models import ServiceType


class ServiceTypeSerializer(serializers.ModelSerializer):
    services_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceType
        fields = [
            'id', 'name', 'description', 'client_types', 'main_image',
            'benefits', 'benefits_images', 'target', 'products', 'slug',
            'services_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'slug']
    
    def get_services_count(self, obj):
        """Количество услуг данного типа"""
        return obj.services.count()
    
    def validate_client_types(self, value):
        """Валидация типов клиентов"""
        if not isinstance(value, list):
            raise serializers.ValidationError("client_types должен быть массивом")
        return value
    
    def validate_benefits(self, value):
        """Валидация преимуществ"""
        if not isinstance(value, list):
            raise serializers.ValidationError("benefits должен быть массивом")
        
        for benefit in value:
            if not isinstance(benefit, dict):
                raise serializers.ValidationError("Каждое преимущество должно быть объектом")
            
            required_fields = ['title', 'text']
            for field in required_fields:
                if field not in benefit:
                    raise serializers.ValidationError(
                        f"Каждое преимущество должно содержать поле '{field}'"
                    )
        
        return value
    
    def validate_products(self, value):
        """Валидация продуктов"""
        if not isinstance(value, list):
            raise serializers.ValidationError("products должен быть массивом")
        
        # Проверяем, что все элементы - числа (ID продуктов)
        for product_id in value:
            if not isinstance(product_id, int):
                raise serializers.ValidationError("Все ID продуктов должны быть числами")
        
        return value


class ServiceTypeListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка типов услуг"""
    services_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceType
        fields = [
            'id', 'name', 'client_types', 'target', 'main_image', 'slug', 'services_count',
        ]
    
    def get_services_count(self, obj):
        return obj.services.count()