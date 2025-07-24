import django_filters
from .models import Service


class ServiceFilter(django_filters.FilterSet):
    service_type_id = django_filters.NumberFilter(field_name='service_type__id')
    price_from_min = django_filters.NumberFilter(field_name='price_from', lookup_expr='gte')
    price_from_max = django_filters.NumberFilter(field_name='price_from', lookup_expr='lte')
    price_to_min = django_filters.NumberFilter(field_name='price_to', lookup_expr='gte')
    price_to_max = django_filters.NumberFilter(field_name='price_to', lookup_expr='lte')
    duration = django_filters.CharFilter(field_name='duration', lookup_expr='icontains')
    
    # Фильтрация по собственным полям услуги
    target = django_filters.CharFilter(field_name='target', lookup_expr='iexact')
    client_types = django_filters.CharFilter(method='filter_client_types')
    
    class Meta:
        model = Service
        fields = ['service_type_id', 'target', 'client_types']
    
    def filter_client_types(self, queryset, name, value):
        """
        Фильтрация по типам клиентов
        Можно передать:
        - один ID: ?client_types=1
        - несколько ID через запятую: ?client_types=1,2,3
        """
        try:
            if ',' in value:
                # Несколько ID через запятую
                client_type_ids = [int(id.strip()) for id in value.split(',')]
                # Ищем услуги, которые содержат любой из указанных ID
                from django.db.models import Q
                query = Q()
                for client_type_id in client_type_ids:
                    query |= Q(client_types__contains=[client_type_id])
                return queryset.filter(query)
            else:
                # Один ID
                client_type_id = int(value)
                return queryset.filter(client_types__contains=[client_type_id])
        except (ValueError, TypeError):
            return queryset.none()