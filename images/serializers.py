from rest_framework import serializers
from .models import ImageUpload


class ImageUploadSerializer(serializers.ModelSerializer):
    compress = serializers.BooleanField(write_only=True, default=True)
    crop = serializers.BooleanField(write_only=True, default=False)
    image_url = serializers.SerializerMethodField()
    cropped_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ImageUpload
        fields = [
            'id', 'original_image', 'processed_image', 'cropped_image',
            'is_compressed', 'is_cropped', 'compress', 'crop',
            'image_url', 'cropped_url', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'processed_image', 'cropped_image', 'is_compressed', 'is_cropped',
            'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        compress = validated_data.pop('compress', True)
        crop = validated_data.pop('crop', False)
        
        image_upload = ImageUpload.objects.create(
            is_compressed=compress,
            is_cropped=crop,
            **validated_data
        )
        
        return image_upload
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.get_image_url():
            return request.build_absolute_uri(obj.get_image_url())
        return obj.get_image_url()
    
    def get_cropped_url(self, obj):
        request = self.context.get('request')
        if request and obj.get_cropped_url():
            return request.build_absolute_uri(obj.get_cropped_url())
        return obj.get_cropped_url()


class ImageListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка изображений"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ImageUpload
        fields = ['id', 'image_url', 'is_compressed', 'is_cropped', 'created_at']
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.get_image_url():
            return request.build_absolute_uri(obj.get_image_url())
        return obj.get_image_url()