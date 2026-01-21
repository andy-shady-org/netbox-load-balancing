from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup
from strawberry.scalars import ID

from netbox.graphql.filters import PrimaryModelFilter
from netbox_load_balancing.graphql.enums import (
    NetBoxLoadBalancingListenerProtocolEnum,
)

from netbox_load_balancing.models import (
    Listener,
)
from netbox_load_balancing.graphql.filters import NetBoxLoadBalancingLBServiceFilter

__all__ = ("NetBoxLoadBalancingListenerFilter",)


@strawberry_django.filter(Listener, lookups=True)
class NetBoxLoadBalancingListenerFilter(PrimaryModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    service: (
        Annotated[
            "NetBoxLoadBalancingLBServiceFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    service_id: ID | None = strawberry_django.filter_field()
    port: FilterLookup[int] | None = strawberry_django.filter_field()
    protocol: (
        Annotated[
            "NetBoxLoadBalancingListenerProtocolEnum",
            strawberry.lazy("netbox_load_balancing.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    source_nat: FilterLookup[bool] | None = strawberry_django.filter_field()
    use_proxy_port: FilterLookup[bool] | None = strawberry_django.filter_field()
    max_clients: FilterLookup[int] | None = strawberry_django.filter_field()
    max_requests: FilterLookup[int] | None = strawberry_django.filter_field()
    client_timeout: FilterLookup[int] | None = strawberry_django.filter_field()
    server_timeout: FilterLookup[int] | None = strawberry_django.filter_field()
    client_keepalive: FilterLookup[bool] | None = strawberry_django.filter_field()
    surge_protection: FilterLookup[bool] | None = strawberry_django.filter_field()
    tcp_buffering: FilterLookup[bool] | None = strawberry_django.filter_field()
    compression: FilterLookup[bool] | None = strawberry_django.filter_field()
