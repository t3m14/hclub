import django_filters
from django.db import models
from .models import ServiceType

class ServiceTypeFilter(django_filters.FilterSet):
    # Кастомный фильтр для JSONField
    client_types = django_filters.CharFilter(method='filter_client_types')
    
    def filter_client_types(self, queryset, name, value):
        # Поиск в JSONField
        return queryset.filter(client_types__icontains=value)
    
    class Meta:
        model = ServiceType
        fields = ['target']
        filter_overrides = {
            models.JSONField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }