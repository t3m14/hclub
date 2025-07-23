from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ServiceType
from .serializers import ServiceTypeSerializer, ServiceTypeListSerializer
from .filters import ServiceTypeFilter
import logging

logger = logging.getLogger(__name__)


class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.prefetch_related('services').all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceTypeFilter
    search_fields = ['name', 'description', 'target']
    ordering_fields = ['name', 'target', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceTypeListSerializer
        return ServiceTypeSerializer
    
    def create(self, request, *args, **kwargs):
        """Создание типа услуги"""
        logger.info(f"Creating service type with data: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            service_type = serializer.save()
            logger.info(f"Service type created successfully: {service_type.id}, slug: {service_type.slug}")
            
            # Используем полный сериализатор для ответа, чтобы включить slug
            response_serializer = ServiceTypeSerializer(service_type, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Service type creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Обновление типа услуги"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        logger.info(f"Updating service type {instance.id} with data: {request.data}")
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            service_type = serializer.save()
            logger.info(f"Service type updated successfully: {service_type.id}, slug: {service_type.slug}")
            
            # Используем полный сериализатор для ответа
            response_serializer = ServiceTypeSerializer(service_type, context={'request': request})
            return Response(response_serializer.data)
        else:
            logger.error(f"Service type update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)