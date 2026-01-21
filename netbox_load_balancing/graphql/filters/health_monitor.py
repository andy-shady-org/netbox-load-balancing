from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filter_lookups import IntegerArrayLookup
from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin
from netbox_load_balancing.graphql.enums import (
    NetBoxLoadBalancingHealthMonitorTypeEnum,
    NetBoxLoadBalancingHealthMonitorHTTPVersionEnum,
)

from netbox_load_balancing.models import (
    HealthMonitor,
)

__all__ = ("NetBoxLoadBalancingHealthMonitorFilter",)


@strawberry_django.filter(HealthMonitor, lookups=True)
class NetBoxLoadBalancingHealthMonitorFilter(ContactFilterMixin, PrimaryModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    template: FilterLookup[str] | None = strawberry_django.filter_field()
    type: (
        Annotated[
            "NetBoxLoadBalancingHealthMonitorTypeEnum",
            strawberry.lazy("netbox_load_balancing.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    monitor_url: FilterLookup[str] | None = strawberry_django.filter_field()
    http_response: FilterLookup[str] | None = strawberry_django.filter_field()
    monitor_host: FilterLookup[str] | None = strawberry_django.filter_field()
    monitor_port: FilterLookup[int] | None = strawberry_django.filter_field()
    http_version: (
        Annotated[
            "NetBoxLoadBalancingHealthMonitorHTTPVersionEnum",
            strawberry.lazy("netbox_load_balancing.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    http_secure: FilterLookup[bool] | None = strawberry_django.filter_field()
    http_response_codes: (
        Annotated[
            "IntegerArrayLookup", strawberry.lazy("netbox.graphql.filter_lookups")
        ]
        | None
    ) = strawberry_django.filter_field()
    probe_interval: FilterLookup[int] | None = strawberry_django.filter_field()
    response_timeout: FilterLookup[int] | None = strawberry_django.filter_field()
    disabled: FilterLookup[bool] | None = strawberry_django.filter_field()
