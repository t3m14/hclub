from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Portfolio
from .serializers import PortfolioSerializer, PortfolioListSerializer
from .filters import PortfolioFilter


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.select_related('service_type', 'service').all()
    
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PortfolioFilter
    search_fields = ['master__name', 'service_type__name', 'service__name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PortfolioListSerializer
        return PortfolioSerializer