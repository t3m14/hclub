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
        try:
            int_value = int(value)
            # Ищем вхождения как в списке, так и в словаре
            list_condition = Q(service_types__contains=[int_value])
            dict_condition = Q(service_types__has_key=str(int_value))
            return queryset.filter(list_condition | dict_condition)
        except (ValueError, TypeError):
            return queryset.none()

    def filter_service_id(self, queryset, name, value):
        try:
            int_value = int(value)
            # Ищем вхождения как в списке, так и в словаре
            list_condition = Q(services__contains=[int_value])
            dict_condition = Q(services__has_key=str(int_value))
            return queryset.filter(list_condition | dict_condition)
        except (ValueError, TypeError):
            return queryset.none()

    def filter_master_name(self, queryset, name, value):
        exact_match = queryset.filter(master__name__iexact=value)
        if exact_match.exists():
            return exact_match
        return queryset.filter(master__name__icontains=value)

    def filter_target(self, queryset, name, value):
        """
        Фильтрация по target типов услуг или услуг
        """
        ServiceType = apps.get_model('service_types', 'ServiceType')
        Service = apps.get_model('services', 'Service')
        
        # Получаем все ID типов услуг с указанным target
        service_type_ids = ServiceType.objects.filter(
            target__iexact=value
        ).values_list('id', flat=True)
        
        # Получаем все ID услуг с указанным target
        service_ids = Service.objects.filter(
            target__iexact=value
        ).values_list('id', flat=True)
        
        # Создаем условия для фильтрации
        conditions = Q()
        
        # Для типов услуг
        for st_id in service_type_ids:
            conditions |= Q(service_types__contains=st_id)
        
        # Для услуг
        for s_id in service_ids:
            conditions |= Q(services__contains=s_id)
        
        return queryset.filter(conditions)