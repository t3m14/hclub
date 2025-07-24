from rest_framework import serializers
from .models import Service
from service_types.models import ServiceType


class ServiceSerializer(serializers.ModelSerializer):
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    service_type_target = serializers.CharField(source='service_type.target', read_only=True)
    service_type_slug = serializers.CharField(source='service_type.slug', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'service_type', 'service_type_name', 'service_type_target',
            'service_type_slug', 'description', 'price_from', 'price_to', 'main_images', 
            'duration', 'steps', 'slug', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'slug']
    
    def validate_service_type(self, value):
        """Проверка существования типа услуги"""
        if not ServiceType.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Тип услуги не найден")
        return value
    
    def validate_main_images(self, value):
        """Валидация главных изображений"""
        if not isinstance(value, list):
            raise serializers.ValidationError("main_images должен быть массивом")
        
        if len(value) > 2:
            raise serializers.ValidationError("Максимум 2 изображения")
        
        return value
    
    def validate_steps(self, value):
        """Валидация этапов услуги"""
        if not isinstance(value, list):
            raise serializers.ValidationError("steps должен быть массивом")
        
        for step in value:
            if not isinstance(step, dict):
                raise serializers.ValidationError("Каждый этап должен быть объектом")
            
            if 'text' not in step:
                raise serializers.ValidationError("Каждый этап должен содержать поле 'text'")
        
        return value
    
    def validate(self, data):
        """Общая валидация"""
        price_from = data.get('price_from')
        price_to = data.get('price_to')
        
        if price_from and price_to and price_from > price_to:
            raise serializers.ValidationError("price_from не может быть больше price_to")
        
        return data


class ServiceListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка услуг"""
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    service_type_slug = serializers.CharField(source='service_type.slug', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'service_type', 'service_type_name', 'service_type_slug',
            'price_from', 'price_to', 'duration', 'slug'
        ]