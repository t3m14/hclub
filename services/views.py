# services/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import Service
from .serializers import ServiceSerializer, ServiceListSerializer
from .filters import ServiceFilter
from utils.pagination import ServicePagination
import logging

logger = logging.getLogger(__name__)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related('service_type').all()
    serializer_class = ServiceSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    pagination_class = ServicePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = [
        'name', 
        'description', 
        'service_type__name',
        'duration',
        'target',  # JSONField
        'client_types',  # JSONField
    ]
    ordering_fields = ['name', 'price_from', 'price_to', 'duration', 'created_at']
    ordering = ['-created_at']
    
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    
    def get_serializer_class(self):
        return ServiceListSerializer if self.action == 'list' else ServiceSerializer
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Creating service with data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = serializer.save()
        logger.info(f"Service created successfully: {service.id}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        logger.info(f"Services list request with filters: {request.query_params}")
        
        # Применяем все фильтры, поиск и сортировку
        queryset = self.filter_queryset(self.get_queryset())
        
        # Получаем общее количество записей ДО пагинации
        full_count = queryset.count()
        
        # Применяем пагинацию
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
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