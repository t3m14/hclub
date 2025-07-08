from rest_framework import serializers
from .models import ServiceType, Service
from products.serializers import ProductSerializer


class ServiceTypeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    products_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = ServiceType
        fields = [
            'id', 'name', 'description', 'client_types', 'main_image',
            'benefits', 'benefits_images', 'target', 'products', 'products_ids',
            'slug', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        products_ids = validated_data.pop('products_ids', [])
        service_type = ServiceType.objects.create(**validated_data)
        
        if products_ids:
            service_type.products.set(products_ids)
        
        return service_type
    
    def update(self, instance, validated_data):
        products_ids = validated_data.pop('products_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if products_ids is not None:
            instance.products.set(products_ids)
        
        return instance


class ServiceSerializer(serializers.ModelSerializer):
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'service_type', 'service_type_name', 'description',
            'price_from', 'price_to', 'main_images', 'duration', 'steps',
            'slug', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']


class ServiceListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка услуг"""
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'service_type', 'service_type_name',
            'price_from', 'price_to', 'duration', 'slug'
        ]