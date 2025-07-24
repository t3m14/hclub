from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import Http404
import os
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
    
    @action(detail=False, methods=['delete'], url_path='slug')
    def delete_by_slug(self, request):
        """
        Удаление изображения по slug (URL)
        DELETE /api/images/slug/?slug=${image_url}
        """
        slug = request.query_params.get('slug')
        
        if not slug:
            return Response(
                {'error': 'Параметр slug обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"=== DELETE /api/images/slug/?slug={slug} ===")
        
        try:
            # Ищем изображение по различным полям URL
            image_upload = None
            
            # Попробуем найти по original_image URL
            images_by_original = ImageUpload.objects.filter(original_image__icontains=slug)
            if images_by_original.exists():
                image_upload = images_by_original.first()
            
            # Если не найдено, попробуем найти по processed_image URL
            if not image_upload:
                images_by_processed = ImageUpload.objects.filter(processed_image__icontains=slug)
                if images_by_processed.exists():
                    image_upload = images_by_processed.first()
            
            # Если не найдено, попробуем найти по cropped_image URL
            if not image_upload:
                images_by_cropped = ImageUpload.objects.filter(cropped_image__icontains=slug)
                if images_by_cropped.exists():
                    image_upload = images_by_cropped.first()
            
            # Если всё ещё не найдено, попробуем найти по части пути
            if not image_upload:
                # Извлекаем имя файла из slug
                filename = os.path.basename(slug)
                images_by_filename = ImageUpload.objects.filter(
                    original_image__icontains=filename
                )
                if images_by_filename.exists():
                    image_upload = images_by_filename.first()
            
            if not image_upload:
                logger.warning(f"Image not found for slug: {slug}")
                return Response(
                    {'error': 'Изображение не найдено'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Удаляем физические файлы
            try:
                if image_upload.original_image and os.path.exists(image_upload.original_image.path):
                    os.remove(image_upload.original_image.path)
                    logger.info(f"Deleted original image file: {image_upload.original_image.path}")
                
                if image_upload.processed_image and os.path.exists(image_upload.processed_image.path):
                    os.remove(image_upload.processed_image.path)
                    logger.info(f"Deleted processed image file: {image_upload.processed_image.path}")
                
                if image_upload.cropped_image and os.path.exists(image_upload.cropped_image.path):
                    os.remove(image_upload.cropped_image.path)
                    logger.info(f"Deleted cropped image file: {image_upload.cropped_image.path}")
            
            except Exception as file_error:
                logger.warning(f"Error deleting files for image {image_upload.id}: {str(file_error)}")
                # Продолжаем удаление записи из БД даже если файлы не удалились
            
            # Удаляем запись из базы данных
            image_id = image_upload.id
            image_upload.delete()
            
            logger.info(f"Image {image_id} deleted successfully by slug: {slug}")
            
            return Response(
                {'message': f'Изображение {image_id} успешно удалено'}, 
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Exception as e:
            logger.error(f"Error deleting image by slug {slug}: {str(e)}")
            return Response(
                {'error': f'Ошибка удаления изображения: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
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
                'delete_by_slug': 'DELETE /api/images/slug/?slug=${image_url}',
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