# serializers.py
from rest_framework import serializers
from django.apps import apps
from .models import Portfolio
import json


class ServiceTypesField(serializers.Field):
    def to_representation(self, value):
        if not value:
            return []
        
        try:
            # Преобразуем Decimal в int для поиска
            int_ids = [int(id) for id in value]
            
            ServiceType = apps.get_model('services', 'ServiceType')
            service_types = ServiceType.objects.filter(id__in=int_ids)
            return [{'id': st.id, 'name': st.name, 'target': st.target} for st in service_types]
        except (LookupError, ImportError):
            # Если модель не найдена, возвращаем только ID (преобразованные в int)
            return [{'id': int(id)} for id in value]
        except (ValueError, TypeError):
            return []

    def to_internal_value(self, data):
        if data is None:
            return []
        if not isinstance(data, list):
            raise serializers.ValidationError("Ожидается список ID для типов услуг")
        
        # Фильтруем только валидные ID и преобразуем в int
        valid_ids = []
        for item in data:
            try:
                valid_ids.append(int(item))
            except (ValueError, TypeError):
                continue
        
        return valid_ids


class ServicesField(serializers.Field):
    def to_representation(self, value):
        if not value:
            return []
        
        try:
            # Преобразуем Decimal в int для поиска
            int_ids = [int(id) for id in value]
            
            Service = apps.get_model('services', 'Service')
            services = Service.objects.filter(id__in=int_ids)
            return [{'id': s.id, 'name': s.name} for s in services]
        except (LookupError, ImportError):
            # Если модель не найдена, возвращаем только ID (преобразованные в int)
            return [{'id': int(id)} for id in value]
        except (ValueError, TypeError):
            return []

    def to_internal_value(self, data):
        if data is None:
            return []
        if not isinstance(data, list):
            raise serializers.ValidationError("Ожидается список ID для услуг")
        
        # Фильтруем только валидные ID и преобразуем в int
        valid_ids = []
        for item in data:
            try:
                valid_ids.append(int(item))
            except (ValueError, TypeError):
                continue
        
        return valid_ids


class PortfolioSerializer(serializers.ModelSerializer):
    service_types = ServiceTypesField(required=False, allow_null=True)
    services = ServicesField(required=False, allow_null=True)
    master_name = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = [
            'id', 'image', 'master', 'master_name', 
            'service_types', 'services', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'master_name']

    def get_master_name(self, obj):
        if isinstance(obj.master, dict):
            return obj.master.get('name', 'Неизвестный мастер')
        return str(obj.master) if obj.master else 'Неизвестный мастер'

    def validate_master(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Master должен быть объектом")
        required_fields = ['name']
        for field in required_fields:
            if field not in value or not value[field]:
                raise serializers.ValidationError(f"Поле '{field}' обязательно для мастера")
        return value

    def validate(self, data):
        if 'service_types' in data and data['service_types'] is None:
            data['service_types'] = []
        if 'services' in data and data['services'] is None:
            data['services'] = []
        return data


class PortfolioListSerializer(serializers.ModelSerializer):
    service_types = ServiceTypesField(read_only=True)
    services = ServicesField(read_only=True)
    master_name = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = ['id', 'image', 'master_name', 'service_types', 'services']

    def get_master_name(self, obj):
        if isinstance(obj.master, dict):
            return obj.master.get('name', 'Неизвестный мастер')
        return str(obj.master) if obj.master else 'Неизвестный мастер'