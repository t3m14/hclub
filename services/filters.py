# services/filters.py
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
        Фильтрация по типам клиентов (теперь строки)
        Можно передать:
        - одну строку: ?client_types=для мужчин
        - несколько строк через запятую: ?client_types=для мужчин,для женщин
        """
        try:
            if ',' in value:
                # Несколько типов клиентов через запятую
                client_types = [ct.strip() for ct in value.split(',')]
                # Ищем услуги, которые содержат любой из указанных типов
                from django.db.models import Q
                query = Q()
                for client_type in client_types:
                    query |= Q(client_types__icontains=client_type)
                return queryset.filter(query)
            else:
                # Один тип клиента
                return queryset.filter(client_types__icontains=value.strip())
        except (ValueError, TypeError):
            return queryset.none()