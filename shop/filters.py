import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Product Name'
    )
    price = django_filters.RangeFilter(
        field_name='price',
        label='Price Range'
    )
    category = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains',
        label='Category'
    )

    class Meta:
        model = Product
        fields = []
