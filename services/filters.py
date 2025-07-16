import django_filters
from .models import Service


class ServiceFilter(django_filters.FilterSet):
    service_type_id = django_filters.NumberFilter(field_name='service_type__id')
    price_from_min = django_filters.NumberFilter(field_name='price_from', lookup_expr='gte')
    price_from_max = django_filters.NumberFilter(field_name='price_from', lookup_expr='lte')
    price_to_min = django_filters.NumberFilter(field_name='price_to', lookup_expr='gte')
    price_to_max = django_filters.NumberFilter(field_name='price_to', lookup_expr='lte')
    duration_min = django_filters.NumberFilter(field_name='duration', lookup_expr='gte')
    duration_max = django_filters.NumberFilter(field_name='duration', lookup_expr='lte')
    
    class Meta:
        model = Service
        fields = ['service_type_id']