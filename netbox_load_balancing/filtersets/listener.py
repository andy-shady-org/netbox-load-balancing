import django_filters
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from netbox.filtersets import PrimaryModelFilterSet
from utilities.filtersets import register_filterset

from netbox_load_balancing.models import Listener, LBService, Pool
from netbox_load_balancing.choices import ListenerProtocolChoices


@register_filterset
class ListenerFilterSet(PrimaryModelFilterSet):
    pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Pool.objects.all(),
        field_name="pool_listeners",
        to_field_name="id",
        label=_("Pool (ID)"),
    )
    service_id = django_filters.ModelMultipleChoiceFilter(
        queryset=LBService.objects.all(),
        field_name="service",
        to_field_name="id",
        label=_("LBService (ID)"),
    )
    service = django_filters.ModelMultipleChoiceFilter(
        queryset=LBService.objects.all(),
        field_name="service__name",
        to_field_name="name",
        label=_("LBService (Name)"),
    )
    protocol = django_filters.MultipleChoiceFilter(
        choices=ListenerProtocolChoices,
        required=False,
    )
    source_nat = django_filters.BooleanFilter()
    use_proxy_port = django_filters.BooleanFilter()
    client_keepalive = django_filters.BooleanFilter()
    surge_protection = django_filters.BooleanFilter()
    tcp_buffering = django_filters.BooleanFilter()
    compression = django_filters.BooleanFilter()

    class Meta:
        model = Listener
        fields = [
            "id",
            "name",
            "description",
            "port",
            "max_clients",
            "max_requests",
            "server_timeout",
            "client_timeout",
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(port=value)
            | Q(max_clients=value)
            | Q(max_requests=value)
            | Q(server_timeout=value)
            | Q(client_timeout=value)
        )
        return queryset.filter(qs_filter)
