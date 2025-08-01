from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer
from .filters import ProductFilter
from utils.pagination import CustomPageNumberPagination


class ProductViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    ViewSet для продуктов (без PUT согласно ТЗ)
    """
    queryset = Product.objects.all()
    
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
    pagination_class = CustomPageNumberPagination  # Добавлена пагинация
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter  # Ваш фильтр
    search_fields = ['brand', 'name', 'purpose']
    ordering_fields = ['brand', 'name', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer