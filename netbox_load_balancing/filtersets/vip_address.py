import django_filters
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet, PrimaryModelFilterSet
from utilities.filtersets import register_filterset

from ipam.models import IPAddress

from netbox_load_balancing.models import (
    VirtualIP,
    VirtualIPPool,
)


@register_filterset
class VirtualIPFilterSet(PrimaryModelFilterSet):
    disabled = django_filters.BooleanFilter()
    route_health_injection = django_filters.BooleanFilter()
    virtual_pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VirtualIPPool.objects.all(),
        field_name="virtual_pool",
        to_field_name="id",
        label=_("Virtual Pool (ID)"),
    )
    virtual_pool = django_filters.ModelMultipleChoiceFilter(
        queryset=VirtualIPPool.objects.all(),
        field_name="virtual_pool__name",
        to_field_name="name",
        label=_("Virtual Pool (Name)"),
    )
    address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=IPAddress.objects.all(),
        field_name="address",
        to_field_name="id",
        label=_("IP Address (ID)"),
    )
    address = django_filters.ModelMultipleChoiceFilter(
        queryset=IPAddress.objects.all(),
        field_name="address__address",
        to_field_name="address",
        label=_("IP Address (Address)"),
    )

    class Meta:
        model = VirtualIP
        fields = ["id", "name", "dns_name", "description"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(dns_name__icontains=value)
            | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)
