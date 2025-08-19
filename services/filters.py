# services/filters.py
import django_filters
from django.db.models import Q
from .models import Service

class ServiceFilter(django_filters.FilterSet):
    @staticmethod
    def filter_target(queryset, name, value):
        try:
            value = value.strip()
            if not value:
                return queryset
                
            if ',' in value:
                targets = [t.strip() for t in value.split(',')]
                query = Q()
                for target in targets:
                    query |= Q(target__contains=[target])
                return queryset.filter(query)
            return queryset.filter(target__contains=[value])
        except (ValueError, TypeError):
            return queryset.none()

    @staticmethod
    def filter_client_types(queryset, name, value):
        try:
            value = value.strip()
            if not value:
                return queryset
                
            if ',' in value:
                client_types = [ct.strip() for ct in value.split(',')]
                query = Q()
                for client_type in client_types:
                    query |= Q(client_types__contains=[client_type])
                return queryset.filter(query)
            return queryset.filter(client_types__contains=[value])
        except (ValueError, TypeError):
            return queryset.none()

    service_type_id = django_filters.NumberFilter(field_name='service_type__id')
    price_from_min = django_filters.NumberFilter(field_name='price_from', lookup_expr='gte')
    price_from_max = django_filters.NumberFilter(field_name='price_from', lookup_expr='lte')
    price_to_min = django_filters.NumberFilter(field_name='price_to', lookup_expr='gte')
    price_to_max = django_filters.NumberFilter(field_name='price_to', lookup_expr='lte')
    duration = django_filters.CharFilter(field_name='duration', lookup_expr='icontains')
    
    target = django_filters.CharFilter(method='filter_target')
    client_types = django_filters.CharFilter(method='filter_client_types')
    
    class Meta:
        model = Service
        fields = ['service_type_id', 'target', 'client_types']