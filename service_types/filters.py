import django_filters
from django.db import models
from .models import ServiceType

class ServiceTypeFilter(django_filters.FilterSet):
    # Кастомный фильтр для JSONField
    client_types = django_filters.CharFilter(method='filter_client_types')
    target = django_filters.CharFilter(method='filter_target')
    def filter_target(self, queryset, name, value):
            """
            Фильтрация по целевой аудитории.
            Можно передать:
            - одну строку: ?target=для мужчин
            - несколько строк через запятую: ?target=для мужчин,для женщин
            """
            try:
                if ',' in value:
                    # Несколько целевых аудиторий через запятую
                    targets = [t.strip() for t in value.split(',')]
                    # Ищем услуги, которые содержат любой из указанных таргетов
                    from django.db.models import Q
                    query = Q()
                    for target in targets:
                        query |= Q(target__icontains=target)
                    return queryset.filter(query)
                else:
                    # Один таргет
                    return queryset.filter(target__icontains=value.strip())
            except (ValueError, TypeError):
                return queryset.none()
            
            
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