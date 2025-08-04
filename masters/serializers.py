from rest_framework import serializers
from .models import Master
from products.serializers import ProductSerializer
from service_types.serializers import ServiceTypeSerializer


class MasterSerializer(serializers.ModelSerializer):
    favorite_product_detail = ProductSerializer(source='favorite_product', read_only=True)
    service_types_detail = ServiceTypeSerializer(source='service_types', many=True, read_only=True)
    service_types_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True,  # Делаем обязательным
        help_text="Список ID типов услуг"
    )
    
    class Meta:
        model = Master
        fields = [
            'id', 'name', 'image', 'job_title', 'favorite_product',
            'favorite_product_detail', 'service_types', 'service_types_detail',
            'service_types_ids', 'experience', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'service_types']
        extra_kwargs = {
            'service_types': {'required': False}  # Делаем service_types не обязательным
        }
    
    def validate_service_types_ids(self, value):
        """Валидация типов услуг"""
        if not value:
            raise serializers.ValidationError("Необходимо указать хотя бы один тип услуги")
        
        # Проверяем, что все ID существуют
        from service_types.models import ServiceType
        existing_ids = ServiceType.objects.filter(id__in=value).values_list('id', flat=True)
        non_existing_ids = set(value) - set(existing_ids)
        
        if non_existing_ids:
            raise serializers.ValidationError(
                f"Типы услуг с ID {list(non_existing_ids)} не найдены"
            )
        
        return value
    
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
    favorite_product_name = serializers.SerializerMethodField()
    favorite_product_id = serializers.IntegerField(source='favorite_product.id', read_only=True)
    
    class Meta:
        model = Master
        fields = [
            'id', 'name', 'image', 'job_title', 'experience', 
            'service_types_names', 'favorite_product_name', 'favorite_product_id'
        ]
    
    def get_service_types_names(self, obj):
        return [st.name for st in obj.service_types.all()]
    
    def get_favorite_product_name(self, obj):
        if obj.favorite_product:
            return f"{obj.favorite_product.brand} - {obj.favorite_product.name}"
        return None