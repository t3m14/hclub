from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ServiceType, Service
from .serializers import (
    ServiceTypeSerializer, ServiceSerializer, ServiceListSerializer
)
from .filters import ServiceTypeFilter, ServiceFilter


class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all().prefetch_related('products')
    serializer_class = ServiceTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceTypeFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related('service_type').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price_from', 'duration', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceSerializer
    
    def list(self, request, *args, **kwargs):
        """Переопределяем list для возврата формата с count и full_count"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Подсчитываем общее количество до пагинации
        full_count = queryset.count()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            
            # Модифицируем ответ согласно ТЗ
            return Response({
                'result': serializer.data,
                'count': len(serializer.data),
                'full_count': full_count
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'result': serializer.data,
            'count': len(serializer.data),
            'full_count': full_count
        })