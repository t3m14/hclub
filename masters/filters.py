
import django_filters
from .models import Master


class MasterFilter(django_filters.FilterSet):
    service_types_ids = django_filters.CharFilter(method='filter_service_types')
    experience_min = django_filters.NumberFilter(field_name='experience', lookup_expr='gte')
    experience_max = django_filters.NumberFilter(field_name='experience', lookup_expr='lte')
    # Новый фильтр по таргету через связанные типы услуг
    target = django_filters.CharFilter(method='filter_by_target')
    
    class Meta:
        model = Master
        fields = ['service_types_ids', 'target']
    
    def filter_service_types(self, queryset, name, value):
        """Фильтрация по типам услуг"""
        try:
            service_type_ids = [int(id.strip()) for id in value.split(',')]
            return queryset.filter(service_types__id__in=service_type_ids).distinct()
        except ValueError:
            return queryset.none()
    
    def filter_by_target(self, queryset, name, value):
        """Фильтрация мастеров по таргету их типов услуг"""
        return queryset.filter(service_types__target__iexact=value).distinct()
