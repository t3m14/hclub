import django_filters
from .models import ServiceType, Service


class ServiceTypeFilter(django_filters.FilterSet):
    client_types = django_filters.CharFilter(method='filter_client_types')
    target = django_filters.ChoiceFilter(choices=ServiceType.TARGET_CHOICES)
    
    class Meta:
        model = ServiceType
        fields = ['client_types', 'target']
    
    def filter_client_types(self, queryset, name, value):
        """Фильтрация по типам клиентов"""
        return queryset.filter(client_types__contains=[value])


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