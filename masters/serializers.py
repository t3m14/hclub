from rest_framework import serializers
from .models import Master
from products.serializers import ProductSerializer
from services.serializers import ServiceTypeSerializer


class MasterSerializer(serializers.ModelSerializer):
    favorite_product_detail = ProductSerializer(source='favorite_product', read_only=True)
    service_types_detail = ServiceTypeSerializer(source='service_types', many=True, read_only=True)
    service_types_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Master
        fields = [
            'id', 'name', 'image', 'job_title', 'favorite_product',
            'favorite_product_detail', 'service_types', 'service_types_detail',
            'service_types_ids', 'experience', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        service_types_ids = validated_data.pop('service_types_ids', [])
        master = Master.objects.create(**validated_data)
        
        if service_types_ids:
            master.service_types.set(service_types_ids)
        
        return master
    
    def update(self, instance, validated_data):
        service_types_ids = validated_data.pop('service_types_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if service_types_ids is not None:
            instance.service_types.set(service_types_ids)
        
        return instance


class MasterListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка мастеров"""
    service_types_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Master
        fields = [
            'id', 'name', 'image', 'job_title', 'experience', 'service_types_names'
        ]
    
    def get_service_types_names(self, obj):
        return [st.name for st in obj.service_types.all()]