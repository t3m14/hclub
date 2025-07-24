# services/serializers.py
from rest_framework import serializers
from .models import Service
from service_types.models import ServiceType


class ServiceSerializer(serializers.ModelSerializer):
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    service_type_target = serializers.CharField(source='service_type.target', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'service_type', 'service_type_name', 'service_type_target',
            'description', 'price_from', 'price_to', 'main_images', 
            'duration', 'steps', 'target', 'client_types',
            'slug', 'created_at', 'updated_at'
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
    
    def validate_client_types(self, value):
        """Валидация типов клиентов - теперь массив строк"""
        if not isinstance(value, list):
            raise serializers.ValidationError("client_types должен быть массивом")
        
        # Проверяем, что все элементы - строки
        for client_type in value:
            if not isinstance(client_type, str):
                raise serializers.ValidationError("Все элементы client_types должны быть строками")
        
        return value
    
    def validate_duration(self, value):
        """Валидация продолжительности как строки"""
        if value is not None and not isinstance(value, str):
            raise serializers.ValidationError("duration должно быть строкой")
        
        if value is not None and len(value.strip()) == 0:
            raise serializers.ValidationError("duration не может быть пустой строкой")
        
        return value
    
    def validate(self, data):
        """Общая валидация"""
        price_from = data.get('price_from')
        price_to = data.get('price_to')
        
        if price_from and price_to and price_from > price_to:
            raise serializers.ValidationError("price_from не может быть больше price_to")
        
        # Валидация положительных значений для цен
        if price_from is not None and price_from < 0:
            raise serializers.ValidationError("price_from должно быть положительным числом")
        
        if price_to is not None and price_to < 0:
            raise serializers.ValidationError("price_to должно быть положительным числом")
        
        return data


class ServiceListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка услуг"""
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    
    class Meta:
        model = Service
        fields = '__all__'