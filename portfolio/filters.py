# filters.py
import django_filters
from .models import Portfolio


class PortfolioFilter(django_filters.FilterSet):
    service_type_id = django_filters.NumberFilter(method='filter_service_type_id')
    service_id = django_filters.NumberFilter(method='filter_service_id')
    master_name = django_filters.CharFilter(method='filter_master_name')

    class Meta:
        model = Portfolio
        fields = ['service_type_id', 'service_id', 'master_name']

    def filter_service_type_id(self, queryset, name, value):
        return queryset.filter(service_types__contains=[value])

    def filter_service_id(self, queryset, name, value):
        return queryset.filter(services__contains=[value])

    def filter_master_name(self, queryset, name, value):
        exact_match = queryset.filter(master__name__iexact=value)
        if exact_match.exists():
            return exact_match
        return queryset.filter(master__name__icontains=value)