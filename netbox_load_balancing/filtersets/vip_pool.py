import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet, PrimaryModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    ContentTypeFilter,
    MultiValueCharFilter,
    MultiValueNumberFilter,
)
from utilities.filtersets import register_filterset

from ipam.models import IPRange

from netbox_load_balancing.models import (
    VirtualIPPool,
    VirtualIPPoolAssignment,
)


@register_filterset
class VirtualIPPoolFilterSet(TenancyFilterSet, PrimaryModelFilterSet):
    disabled = django_filters.BooleanFilter()

    class Meta:
        model = VirtualIPPool
        fields = ["id", "name", "description"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(description__icontains=value)
        return queryset.filter(qs_filter)


class VirtualIPPoolAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    disabled = django_filters.BooleanFilter()
    weight = django_filters.BooleanFilter()
    virtual_pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VirtualIPPool.objects.all(),
        label=_("VirtualIPPool (ID)"),
    )
    iprange = MultiValueCharFilter(
        method="filter_address",
        field_name="address",
        label=_("IP Range (Start Address)"),
    )
    iprange_id = MultiValueNumberFilter(
        method="filter_address",
        field_name="pk",
        label=_("IP Range (ID)"),
    )

    class Meta:
        model = VirtualIPPoolAssignment
        fields = (
            "id",
            "disabled",
            "weight",
            "virtual_pool_id",
            "assigned_object_type",
            "assigned_object_id",
        )

    def filter_address(self, queryset, name, value):
        if not (addresses := IPRange.objects.filter(**{f"{name}__in": value})).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(IPRange),
            assigned_object_id__in=addresses.values_list("id", flat=True),
        )
