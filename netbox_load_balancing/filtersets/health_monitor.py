import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet, PrimaryModelFilterSet
from utilities.filters import (
    ContentTypeFilter,
    MultiValueCharFilter,
    MultiValueNumberFilter,
    NumericArrayFilter,
)
from utilities.filtersets import register_filterset

from netbox_load_balancing.models import (
    HealthMonitor,
    HealthMonitorAssignment,
    Pool,
)
from netbox_load_balancing.choices import (
    HealthMonitorTypeChoices,
    HealthMonitorHTTPVersionChoices,
)


@register_filterset
class HealthMonitorFilterSet(PrimaryModelFilterSet):
    type = django_filters.MultipleChoiceFilter(
        choices=HealthMonitorTypeChoices,
        required=False,
    )
    http_version = django_filters.MultipleChoiceFilter(
        choices=HealthMonitorHTTPVersionChoices,
        required=False,
    )
    http_response_codes = NumericArrayFilter(
        field_name="http_response_codes", lookup_expr="contains"
    )
    disabled = django_filters.BooleanFilter()
    http_secure = django_filters.BooleanFilter()

    class Meta:
        model = HealthMonitor
        fields = [
            "id",
            "name",
            "description",
            "template",
            "monitor_url",
            "http_response",
            "monitor_host",
            "monitor_port",
            "probe_interval",
            "response_timeout",
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(template__icontains=value)
            | Q(monitor_url__icontains=value)
            | Q(http_response__icontains=value)
            | Q(monitor_host__icontains=value)
            | Q(monitor_port=value)
            | Q(probe_interval=value)
            | Q(response_timeout=value)
        )
        return queryset.filter(qs_filter)


class HealthMonitorAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    disabled = django_filters.BooleanFilter()
    weight = django_filters.BooleanFilter()
    monitor_id = django_filters.ModelMultipleChoiceFilter(
        queryset=HealthMonitor.objects.all(),
        label=_("Health Monitor (ID)"),
    )
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

    class Meta:
        model = HealthMonitorAssignment
        fields = (
            "id",
            "monitor_id",
            "disabled",
            "weight",
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
