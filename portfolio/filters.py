# filters.py
import django_filters
from django.db.models import Q
from .models import Portfolio
from django.apps import apps


class PortfolioFilter(django_filters.FilterSet):
    service_type_id = django_filters.NumberFilter(method='filter_service_type_id')
    service_id = django_filters.NumberFilter(method='filter_service_id')
    master_name = django_filters.CharFilter(method='filter_master_name')
    target = django_filters.CharFilter(method='filter_target')

    class Meta:
        model = Portfolio
        fields = ['service_type_id', 'service_id', 'master_name', 'target']

    def filter_service_type_id(self, queryset, name, value):
        return queryset.filter(service_types__contains=[value])

    def filter_service_id(self, queryset, name, value):
        return queryset.filter(services__contains=[value])

    def filter_master_name(self, queryset, name, value):
        exact_match = queryset.filter(master__name__iexact=value)
        if exact_match.exists():
            return exact_match
        return queryset.filter(master__name__icontains=value)

    def filter_target(self, queryset, name, value):
        """
        Фильтрация по target, который находится внутри service_types.
        Ищем портфолио, у которых хотя бы один service_type имеет указанный target.
        """
        # Получаем модель ServiceType из правильного приложения
        ServiceType = apps.get_model('services', 'ServiceType')
        
        # Получаем все ID типов услуг с указанным target
        service_type_ids = ServiceType.objects.filter(
            target__iexact=value
        ).values_list('id', flat=True)
        
        # Создаем условия для фильтрации по каждому ID
        conditions = Q()
        for st_id in service_type_ids:
            conditions |= Q(service_types__contains=[st_id])
        
        return queryset.filter(conditions)