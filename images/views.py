from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import ImageUpload
from .serializers import ImageUploadSerializer, ImageListSerializer
import logging

logger = logging.getLogger(__name__)


class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    # Явно определяем разрешенные HTTP методы
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ImageListSerializer
        return ImageUploadSerializer
    
    def get_permissions(self):
        """
        Возвращает разрешения для действий
        """
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        """
        Создание нового изображения
        POST /api/images/
        """
        logger.info("=== POST /api/images/ ===")
        logger.info(f"User: {request.user}")
        logger.info(f"Is authenticated: {request.user.is_authenticated}")
        logger.info(f"Request data keys: {list(request.data.keys())}")
        logger.info(f"Request files: {list(request.FILES.keys())}")
        logger.info(f"Content-Type: {request.content_type}")
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                image_upload = serializer.save()
                logger.info(f"Image created successfully: {image_upload.id}")
                
                # Формируем ответ
                response_data = {
                    'id': image_upload.id,
                    'original_url': request.build_absolute_uri(image_upload.original_image.url),
                    'image_url': request.build_absolute_uri(image_upload.get_image_url()) if image_upload.get_image_url() else None,
                    'cropped_url': request.build_absolute_uri(image_upload.get_cropped_url()) if image_upload.get_cropped_url() else None,
                    'is_compressed': image_upload.is_compressed,
                    'is_cropped': image_upload.is_cropped,
                    'created_at': image_upload.created_at,
                }
                
                return Response(response_data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Error creating image: {str(e)}")
                return Response(
                    {'error': f'Ошибка создания изображения: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            logger.error(f"Serializer validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def debug_routes(self, request):
        """
        Отладочный эндпоинт
        GET /api/images/debug/
        """
        return Response({
            'message': 'Images API is working',
            'available_methods': self.http_method_names,
            'current_user': str(request.user),
            'is_authenticated': request.user.is_authenticated,
            'viewset_class': self.__class__.__name__,
            'actions': {
                'list': 'GET /api/images/',
                'create': 'POST /api/images/',
                'retrieve': 'GET /api/images/{id}/',
                'update': 'PUT /api/images/{id}/',
                'partial_update': 'PATCH /api/images/{id}/',
                'destroy': 'DELETE /api/images/{id}/',
                'debug_routes': 'GET /api/images/debug/',
            }
        })
    
    def list(self, request, *args, **kwargs):
        """
        Список изображений
        GET /api/images/
        """
        logger.info("=== GET /api/images/ ===")
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Получение изображения по ID
        GET /api/images/{id}/
        """
        logger.info(f"=== GET /api/images/{kwargs.get('pk')}/ ===")
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Обновление изображения
        PUT /api/images/{id}/
        """
        logger.info(f"=== PUT /api/images/{kwargs.get('pk')}/ ===")
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Частичное обновление изображения
        PATCH /api/images/{id}/
        """
        logger.info(f"=== PATCH /api/images/{kwargs.get('pk')}/ ===")
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Удаление изображения
        DELETE /api/images/{id}/
        """
        logger.info(f"=== DELETE /api/images/{kwargs.get('pk')}/ ===")
        return super().destroy(request, *args, **kwargs)