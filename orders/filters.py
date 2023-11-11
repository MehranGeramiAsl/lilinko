import django_filters
from orders.models import LinkOrder


class OrderFilter(django_filters.FilterSet):
    buyer_status = django_filters.CharFilter(field_name="buyer_status",lookup_expr="exact")
    seller_status = django_filters.CharFilter(field_name="seller_status",lookup_expr="exact")
    price = django_filters.CharFilter(field_name="initial_price",lookup_expr="exact")
    proposed_title =django_filters.CharFilter(field_name="proposed_title",lookup_expr="icontains")
    proposed_content = django_filters.CharFilter(field_name="proposed_content",lookup_expr="icontains")
    backlink = django_filters.CharFilter(field_name="backlink",lookup_expr="icontains")
    anchor_text = django_filters.CharFilter(field_name="anchor_text",lookup_expr="icontains")
    proposed_meta_title = django_filters.CharFilter(field_name="proposed_meta_title",lookup_expr="icontains")
    proposed_meta_description = django_filters.CharFilter(field_name="proposed_meta_description")
    is_submited = django_filters.BooleanFilter(field_name="is_submited")
    link = django_filters.CharFilter(field_name="link_provider__link__url",lookup_expr="icontains")



    class Meta:
        model = LinkOrder
        fields = "__all__"