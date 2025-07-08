import django_filters
from .models import Master


class MasterFilter(django_filters.FilterSet):
    service_types_ids = django_filters.CharFilter(method='filter_service_types')
    experience_min = django_filters.NumberFilter(field_name='experience', lookup_expr='gte')
    experience_max = django_filters.NumberFilter(field_name='experience', lookup_expr='lte')
    
    class Meta:
        model = Master
        fields = ['service_types_ids']
    
    def filter_service_types(self, queryset, name, value):
        """Фильтрация по типам услуг"""
        try:
            service_type_ids = [int(id.strip()) for id in value.split(',')]
            return queryset.filter(service_types__id__in=service_type_ids).distinct()
        except ValueError:
            return queryset.none()