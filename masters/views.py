from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Master
from .serializers import MasterSerializer, MasterListSerializer
from .filters import MasterFilter
from utils.pagination import CustomPageNumberPagination  # Добавляем пагинацию
import logging

logger = logging.getLogger(__name__)


class MasterViewSet(viewsets.ModelViewSet):
    queryset = Master.objects.prefetch_related('service_types', 'favorite_product').all()
    serializer_class = MasterSerializer
    
    def get_permissions(self):
        """
        Определение разрешений для разных действий.
        GET запросы доступны всем, остальные требуют авторизации.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    pagination_class = CustomPageNumberPagination  # Добавляем пагинацию
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MasterFilter
    search_fields = ['name', 'job_title']
    ordering_fields = ['name', 'experience', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MasterListSerializer
        return MasterSerializer
    
    def create(self, request, *args, **kwargs):
        """Создание мастера"""
        logger.info(f"Creating master with data: {request.data}")
        if 'experience' in request.data and request.data['experience'] is None:
            request.data['experience'] = None  # Явно устанавливаем None
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            master = serializer.save()
            logger.info(f"Master created successfully: {master.id}")
            
            # Используем полный сериализатор для ответа
            response_serializer = MasterSerializer(master, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Master creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Обновление мастера"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        logger.info(f"Updating master {instance.id} with data: {request.data}")
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            master = serializer.save()
            logger.info(f"Master updated successfully: {master.id}")
            
            # Используем полный сериализатор для ответа
            response_serializer = MasterSerializer(master, context={'request': request})
            return Response(response_serializer.data)
        else:
            logger.error(f"Master update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)