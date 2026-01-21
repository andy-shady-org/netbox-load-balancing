import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet, PrimaryModelFilterSet
from utilities.filters import (
    ContentTypeFilter,
    MultiValueCharFilter,
    MultiValueNumberFilter,
)
from utilities.filtersets import register_filterset

from ipam.models import IPAddress

from netbox_load_balancing.models import (
    Member,
    MemberAssignment,
    Pool,
    HealthMonitor,
)


@register_filterset
class MemberFilterSet(PrimaryModelFilterSet):
    ip_address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=IPAddress.objects.all(),
        field_name="ip_address",
        to_field_name="id",
        label=_("Listener (ID)"),
    )
    ip_address = django_filters.ModelMultipleChoiceFilter(
        queryset=IPAddress.objects.all(),
        field_name="ip_address__address",
        to_field_name="address",
        label=_("Listener (Address)"),
    )
    disabled = django_filters.BooleanFilter()

    class Meta:
        model = Member
        fields = ["id", "name", "description", "reference"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(reference__icontains=value)
        )
        return queryset.filter(qs_filter)


class MemberAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    member_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Member.objects.all(),
        label=_("Member (ID)"),
    )
    disabled = django_filters.BooleanFilter()
    pool = MultiValueCharFilter(
        method="filter_pool",
        field_name="name",
        label=_("Pool (Name)"),
    )
    pool_id = MultiValueNumberFilter(
        method="filter_pool",
        field_name="pk",
        label=_("Pool (ID)"),
    )
    healthmonitor = MultiValueCharFilter(
        method="filter_health_monitor",
        field_name="name",
        label=_("Health Monitor (Name)"),
    )
    healthmonitor_id = MultiValueNumberFilter(
        method="filter_health_monitor",
        field_name="pk",
        label=_("Health Monitor (ID)"),
    )

    class Meta:
        model = MemberAssignment
        fields = (
            "id",
            "member_id",
            "disabled",
            "assigned_object_type",
            "assigned_object_id",
        )

    def filter_pool(self, queryset, name, value):
        if not (pools := Pool.objects.filter(**{f"{name}__in": value})).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(Pool),
            assigned_object_id__in=pools.values_list("id", flat=True),
        )

    def filter_health_monitor(self, queryset, name, value):
        if not (
            pools := HealthMonitor.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(HealthMonitor),
            assigned_object_id__in=pools.values_list("id", flat=True),
        )
