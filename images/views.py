from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import Http404
from drf_spectacular.utils import extend_schema_view, extend_schema
import os
from .models import ImageUpload
from .serializers import ImageUploadSerializer, ImageListSerializer
import logging

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(description="Получение списка изображений"),
    create=extend_schema(description="Загрузка нового изображения"),
    retrieve=extend_schema(description="Получение изображения по ID"),
    update=extend_schema(description="Обновление изображения"),
    partial_update=extend_schema(description="Частичное обновление изображения"),
    destroy=extend_schema(description="Удаление изображения по ID"),
)
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
    
    @extend_schema(
        description="Поиск изображения по slug (URL) без удаления",
        parameters=[
            {
                'name': 'slug',
                'in': 'query',
                'description': 'URL изображения или его часть',
                'required': True,
                'schema': {'type': 'string'}
            }
        ],
        responses={
            200: {'description': 'Изображение найдено'},
            400: {'description': 'Параметр slug обязателен'},
            404: {'description': 'Изображение не найдено'}
        }
    )
    @action(detail=False, methods=['get'], url_path='find')
    def find_by_slug(self, request):
        """
        Поиск изображения по slug (URL) без удаления
        GET /api/images/find/?slug=${image_url}
        """
        slug = request.query_params.get('slug')
        
        if not slug:
            return Response(
                {'error': 'Параметр slug обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f"=== GET /api/images/find/?slug={slug} ===")
        
        try:
            # Используем ту же логику поиска, что и в delete_by_slug
            image_upload = None
            filename = os.path.basename(slug)
            filename_without_ext = os.path.splitext(filename)[0]
            
            logger.info(f"Searching for image with slug: {slug}")
            logger.info(f"Extracted filename: {filename}")
            logger.info(f"Filename without extension: {filename_without_ext}")
            
            # Поиск по original_image
            images_by_original = ImageUpload.objects.filter(original_image__icontains=filename)
            if images_by_original.exists():
                image_upload = images_by_original.first()
                logger.info(f"Found by original_image: {image_upload.id}")
            
            # Поиск по processed_image
            if not image_upload:
                images_by_processed = ImageUpload.objects.filter(processed_image__icontains=filename)
                if images_by_processed.exists():
                    image_upload = images_by_processed.first()
                    logger.info(f"Found by processed_image: {image_upload.id}")
            
            # Поиск по cropped_image
            if not image_upload:
                images_by_cropped = ImageUpload.objects.filter(cropped_image__icontains=filename)
                if images_by_cropped.exists():
                    image_upload = images_by_cropped.first()
                    logger.info(f"Found by cropped_image: {image_upload.id}")
            
            # Поиск по части имени без расширения
            if not image_upload:
                images_by_filename_part = ImageUpload.objects.filter(
                    original_image__icontains=filename_without_ext
                )
                if images_by_filename_part.exists():
                    image_upload = images_by_filename_part.first()
                    logger.info(f"Found by filename part: {image_upload.id}")
            
            if not image_upload:
                images_by_processed_part = ImageUpload.objects.filter(
                    processed_image__icontains=filename_without_ext
                )
                if images_by_processed_part.exists():
                    image_upload = images_by_processed_part.first()
                    logger.info(f"Found by processed filename part: {image_upload.id}")
            
            # Дополнительный поиск
            if not image_upload:
                for img in ImageUpload.objects.all():
                    if (img.original_image and filename_without_ext in img.original_image.name) or \
                       (img.processed_image and filename_without_ext in img.processed_image.name) or \
                       (img.cropped_image and filename_without_ext in img.cropped_image.name):
                        image_upload = img
                        logger.info(f"Found by manual search: {image_upload.id}")
                        break
            
            if not image_upload:
                logger.warning(f"Image not found for slug: {slug}")
                return Response(
                    {'error': 'Изображение не найдено'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Возвращаем информацию о найденном изображении
            return Response({
                'found': True,
                'image': {
                    'id': image_upload.id,
                    'original_image': image_upload.original_image.name if image_upload.original_image else None,
                    'processed_image': image_upload.processed_image.name if image_upload.processed_image else None,
                    'cropped_image': image_upload.cropped_image.name if image_upload.cropped_image else None,
                    'original_url': request.build_absolute_uri(image_upload.original_image.url) if image_upload.original_image else None,
                    'processed_url': request.build_absolute_uri(image_upload.processed_image.url) if image_upload.processed_image else None,
                    'cropped_url': request.build_absolute_uri(image_upload.cropped_image.url) if image_upload.cropped_image else None,
                    'is_compressed': image_upload.is_compressed,
                    'is_cropped': image_upload.is_cropped,
                    'created_at': image_upload.created_at,
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error finding image by slug {slug}: {str(e)}")
            return Response(
                {'error': f'Ошибка поиска изображения: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        description="Удаление изображения по slug (URL)",
        parameters=[
            {
                'name': 'slug',
                'in': 'query',
                'description': 'URL изображения или его часть',
                'required': True,
                'schema': {'type': 'string'}
            }
        ],
        responses={
            204: {'description': 'Изображение успешно удалено'},
            400: {'description': 'Параметр slug обязателен'},
            404: {'description': 'Изображение не найдено'},
            500: {'description': 'Ошибка сервера'}
        }
    )
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
            
            # Извлекаем имя файла из slug для более точного поиска
            filename = os.path.basename(slug)
            # Убираем расширение для поиска
            filename_without_ext = os.path.splitext(filename)[0]
            
            logger.info(f"Searching for image with slug: {slug}")
            logger.info(f"Extracted filename: {filename}")
            logger.info(f"Filename without extension: {filename_without_ext}")
            
            # Попробуем найти по имени файла в original_image
            images_by_original = ImageUpload.objects.filter(original_image__icontains=filename)
            if images_by_original.exists():
                image_upload = images_by_original.first()
                logger.info(f"Found by original_image: {image_upload.id}")
            
            # Если не найдено, попробуем найти по processed_image
            if not image_upload:
                images_by_processed = ImageUpload.objects.filter(processed_image__icontains=filename)
                if images_by_processed.exists():
                    image_upload = images_by_processed.first()
                    logger.info(f"Found by processed_image: {image_upload.id}")
            
            # Если не найдено, попробуем найти по cropped_image
            if not image_upload:
                images_by_cropped = ImageUpload.objects.filter(cropped_image__icontains=filename)
                if images_by_cropped.exists():
                    image_upload = images_by_cropped.first()
                    logger.info(f"Found by cropped_image: {image_upload.id}")
            
            # Если всё ещё не найдено, попробуем найти по части имени без расширения
            if not image_upload:
                images_by_filename_part = ImageUpload.objects.filter(
                    original_image__icontains=filename_without_ext
                )
                if images_by_filename_part.exists():
                    image_upload = images_by_filename_part.first()
                    logger.info(f"Found by filename part: {image_upload.id}")
            
            # Если всё ещё не найдено, попробуем найти по processed файлу без расширения
            if not image_upload:
                images_by_processed_part = ImageUpload.objects.filter(
                    processed_image__icontains=filename_without_ext
                )
                if images_by_processed_part.exists():
                    image_upload = images_by_processed_part.first()
                    logger.info(f"Found by processed filename part: {image_upload.id}")
            
            # Дополнительный поиск: по ID из имени файла (если имя содержит ID)
            if not image_upload:
                # Попробуем извлечь ID из имени файла (например, "3dcab0ad" может быть частью ID или хеша)
                for img in ImageUpload.objects.all():
                    if (img.original_image and filename_without_ext in img.original_image.name) or \
                       (img.processed_image and filename_without_ext in img.processed_image.name) or \
                       (img.cropped_image and filename_without_ext in img.cropped_image.name):
                        image_upload = img
                        logger.info(f"Found by manual search: {image_upload.id}")
                        break
            
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
    
    @extend_schema(
        description="Отладочная информация об API изображений",
        responses={200: {'description': 'Информация о доступных действиях'}}
    )
    @action(detail=False, methods=['get'])
    def debug_routes(self, request):
        """
        Отладочный эндпоинт
        GET /api/images/debug/
        """
        # Получаем информацию о всех изображениях для отладки
        images_info = []
        for img in ImageUpload.objects.all()[:5]:  # Первые 5 для примера
            images_info.append({
                'id': img.id,
                'original_image': img.original_image.name if img.original_image else None,
                'processed_image': img.processed_image.name if img.processed_image else None,
                'cropped_image': img.cropped_image.name if img.cropped_image else None,
                'original_url': img.original_image.url if img.original_image else None,
                'processed_url': img.processed_image.url if img.processed_image else None,
                'cropped_url': img.cropped_image.url if img.cropped_image else None,
            })
        
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
            },
            'sample_images': images_info
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