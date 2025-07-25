from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Service
from .serializers import ServiceSerializer, ServiceListSerializer
from .filters import ServiceFilter
from utils.pagination import ServicePagination
import logging

logger = logging.getLogger(__name__)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related('service_type').all()
    serializer_class = ServiceSerializer
    pagination_class = ServicePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['name', 'description', 'service_type__name', 'target']
    ordering_fields = ['name', 'price_from', 'price_to', 'duration', 'target', 'created_at']
    ordering = ['-created_at']
    
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceSerializer
    
    def create(self, request, *args, **kwargs):
        """Создание услуги"""
        logger.info(f"Creating service with data: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save()
            logger.info(f"Service created successfully: {service.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Service creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        """Список услуг с кастомным форматом пагинации"""
        logger.info(f"Services list request with filters: {request.query_params}")
        
        queryset = self.filter_queryset(self.get_queryset())
        
        # Получаем общее количество записей
        full_count = queryset.count()
        
        # Применяем пагинацию
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Возвращаем кастомный формат согласно ТЗ
            return Response({
                'result': serializer.data,
                'count': len(serializer.data),
                'full_count': full_count
            })
        
        # Если пагинация не применена
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'result': serializer.data,
            'count': len(serializer.data),
            'full_count': full_count
        })