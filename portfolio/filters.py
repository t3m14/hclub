# filters.py
import django_filters
from django.db.models import Q
from .models import Portfolio
from django.db.models import Func, Value, BooleanField
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.expressions import ArraySubquery
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
        Используем префиetch для эффективной загрузки связанных данных.
        """
        # Аннотируем queryset флагом, указывающим на наличие service_type с нужным target
        ServiceType = apps.get_model('services', 'ServiceType')
        
        # Создаем подзапрос для определения наличия service_type с нужным target
        service_types_with_target = ServiceType.objects.filter(
            target__iexact=value
        ).values_list('id', flat=True)
        
        # Используем аннотацию для фильтрации
        return queryset.annotate(
            has_target=Exists(
                Portfolio.service_types.intersection(service_types_with_target)
            )
        ).filter(has_target=True)