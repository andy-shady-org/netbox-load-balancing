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

from ipam.models import IPRange

from netbox_load_balancing.models import (
    Pool,
    PoolAssignment,
    Listener,
)
from netbox_load_balancing.choices import (
    PoolAlgorythmChoices,
    PoolSessionPersistenceChoices,
    PoolBackupSessionPersistenceChoices,
)


@register_filterset
class PoolFilterSet(PrimaryModelFilterSet):
    listener_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Listener.objects.all(),
        field_name="listeners",
        to_field_name="id",
        label=_("Listener (ID)"),
    )
    listener = django_filters.ModelMultipleChoiceFilter(
        queryset=Listener.objects.all(),
        field_name="listeners__name",
        to_field_name="name",
        label=_("Listener (Name)"),
    )
    algorythm = django_filters.MultipleChoiceFilter(
        choices=PoolAlgorythmChoices,
        required=False,
    )
    session_persistence = django_filters.MultipleChoiceFilter(
        choices=PoolSessionPersistenceChoices,
        required=False,
    )
    backup_persistence = django_filters.MultipleChoiceFilter(
        choices=PoolBackupSessionPersistenceChoices,
        required=False,
    )
    disabled = django_filters.BooleanFilter()

    class Meta:
        model = Pool
        fields = [
            "id",
            "name",
            "description",
            "persistence_timeout",
            "backup_timeout",
            "member_port",
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(persistence_timeout=value)
            | Q(dbackup_timeout=value)
            | Q(member_port=value)
        )
        return queryset.filter(qs_filter)


class PoolAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Pool.objects.all(),
        label=_("Pool (ID)"),
    )
    ip_range = MultiValueCharFilter(
        method="filter_range",
        field_name="start_address",
        label=_("IP Range (Start Address)"),
    )
    ip_range_id = MultiValueNumberFilter(
        method="filter_range",
        field_name="pk",
        label=_("IP Range (ID)"),
    )

    class Meta:
        model = PoolAssignment
        fields = ("id", "pool_id", "assigned_object_type", "assigned_object_id")

    def filter_range(self, queryset, name, value):
        if not (ranges := IPRange.objects.filter(**{f"{name}__in": value})).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(IPRange),
            assigned_object_id__in=ranges.values_list("id", flat=True),
        )
