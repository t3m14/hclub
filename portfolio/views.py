from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Portfolio
from .serializers import PortfolioSerializer, PortfolioListSerializer
from .filters import PortfolioFilter
from utils.pagination import CustomPageNumberPagination  # Добавляем пагинацию


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.select_related('service_type', 'service').all()
    pagination_class = CustomPageNumberPagination  # Добавляем пагинацию
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PortfolioFilter
    search_fields = ['master__name', 'service_type__name', 'service__name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PortfolioListSerializer
        return PortfolioSerializer