from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ImageUpload
from .serializers import ImageUploadSerializer, ImageListSerializer


class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ImageListSerializer
        return ImageUploadSerializer
    
    def create(self, request, *args, **kwargs):
        """Создание изображения с обработкой"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            image_upload = serializer.save()
            
            # Возвращаем URL изображений
            response_data = {
                'id': image_upload.id,
                'original_url': request.build_absolute_uri(image_upload.original_image.url),
                'image_url': request.build_absolute_uri(image_upload.get_image_url()) if image_upload.get_image_url() else None,
                'cropped_url': request.build_absolute_uri(image_upload.get_cropped_url()) if image_upload.get_cropped_url() else None,
                'is_compressed': image_upload.is_compressed,
                'is_cropped': image_upload.is_cropped,
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)