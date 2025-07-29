import django_filters
from .models import Portfolio


class PortfolioFilter(django_filters.FilterSet):
    master_name = django_filters.CharFilter(method='filter_master_name')
    service_type_id = django_filters.NumberFilter(field_name='service_type__id')
    service_id = django_filters.NumberFilter(field_name='service__id')
    target = django_filters.CharFilter(field_name='service_type__target')
    
    class Meta:
        model = Portfolio
        fields = ['service_type_id', 'service_id', 'target', 'master_name']
    
    def filter_master_name(self, queryset, name, value):
        """Фильтрация по имени мастера (точное и частичное совпадение)"""
        # Поиск по точному совпадению имени
        exact_match = queryset.filter(master__name__iexact=value)
        if exact_match.exists():
            return exact_match
        
        # Если точного совпадения нет, ищем по частичному
        return queryset.filter(master__name__icontains=value)