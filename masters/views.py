from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Master
from .serializers import MasterSerializer, MasterListSerializer
from .filters import MasterFilter


class MasterViewSet(viewsets.ModelViewSet):
    queryset = Master.objects.prefetch_related('service_types', 'favorite_product').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MasterFilter
    search_fields = ['name', 'job_title']
    ordering_fields = ['name', 'experience', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MasterListSerializer
        return MasterSerializer