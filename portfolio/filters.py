import django_filters
from .models import Portfolio


class PortfolioFilter(django_filters.FilterSet):
    master_name = django_filters.CharFilter(method='filter_master_name')
    service_type_id = django_filters.NumberFilter(field_name='service_type__id')
    service_id = django_filters.NumberFilter(field_name='service__id')
    target = django_filters.CharFilter(field_name='service_type__target')
    
    class Meta:
        model = Portfolio
        fields = ['service_type_id', 'service_id']
    
    def filter_master_name(self, queryset, name, value):
        """Фильтрация по имени мастера"""
        return queryset.filter(master__name__icontains=value)