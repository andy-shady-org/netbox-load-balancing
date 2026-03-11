from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filter_lookups import IntegerArrayLookup, IntegerLookup
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
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    template: StrFilterLookup[str] | None = strawberry_django.filter_field()
    type: (
        Annotated[
            "NetBoxLoadBalancingHealthMonitorTypeEnum",
            strawberry.lazy("netbox_load_balancing.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    monitor_url: StrFilterLookup[str] | None = strawberry_django.filter_field()
    http_response: StrFilterLookup[str] | None = strawberry_django.filter_field()
    monitor_host: StrFilterLookup[str] | None = strawberry_django.filter_field()
    monitor_port: (
        Annotated["IntegerLookup", strawberry.lazy("netbox.graphql.filter_lookups")]
        | None
    ) = strawberry_django.filter_field()
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
    probe_interval: (
        Annotated["IntegerLookup", strawberry.lazy("netbox.graphql.filter_lookups")]
        | None
    ) = strawberry_django.filter_field()
    response_timeout: (
        Annotated["IntegerLookup", strawberry.lazy("netbox.graphql.filter_lookups")]
        | None
    ) = strawberry_django.filter_field()
    disabled: FilterLookup[bool] | None = strawberry_django.filter_field()
