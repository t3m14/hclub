import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    # Точное совпадение по предназначению
    purpose = django_filters.CharFilter(field_name='purpose', lookup_expr='exact')
    
    # # Поиск по части названия предназначения (может быть полезно)
    # purpose_contains = django_filters.CharFilter(field_name='purpose', lookup_expr='icontains')
    
    # # Фильтр по бренду
    # brand = django_filters.CharFilter(field_name='brand', lookup_expr='exact')
    # brand_contains = django_filters.CharFilter(field_name='brand', lookup_expr='icontains')
    
    # # Фильтр по названию продукта
    # name = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    # name_contains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    class Meta:
        model = Product
        fields = ['purpose', 'brand', 'name']