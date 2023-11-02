import django_filters
from links.models import Link


class LinkFilter(django_filters.FilterSet):
    url = django_filters.CharFilter(field_name="url",lookup_expr="icontains")
    categories = django_filters.CharFilter(method="filter_by_categories")
    price = django_filters.RangeFilter()
    traffic = django_filters.RangeFilter()
    dr = django_filters.RangeFilter()
    

    def filter_by_categories(self,queryset,name,value):
        return queryset.filter(linkcategories__title__icontains = value)
    
    class Meta:
        model = Link
        fields = ["url","categories","price","traffic","dr"]