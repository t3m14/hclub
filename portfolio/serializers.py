from rest_framework import serializers
from .models import Portfolio


class PortfolioSerializer(serializers.ModelSerializer):
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_type_target = serializers.CharField(source='service_type.target', read_only=True)
    
    class Meta:
        model = Portfolio
        fields = [
            'id', 'image', 'master', 'service_type', 'service_type_name',
            'service_type_target', 'service', 'service_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_master(self, value):
        """Валидация поля master"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Master должен быть объектом")
        
        required_fields = ['name']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f"Поле '{field}' обязательно для мастера")
        
        return value


class PortfolioListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка портфолио"""
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    master_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Portfolio
        fields = [
            'id', 'image', 'master_name', 'service_type_name', 'service_name'
        ]
    
    def get_master_name(self, obj):
        if isinstance(obj.master, dict):
            return obj.master.get('name', 'Неизвестный мастер')
        return str(obj.master)