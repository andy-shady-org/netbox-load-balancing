from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup
from strawberry.scalars import ID

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin
from ipam.graphql.filters import IPAddressFilter

from netbox_load_balancing.models import (
    VirtualIP,
)
from netbox_load_balancing.graphql.filters import NetBoxLoadBalancingVirtualIPPoolFilter

__all__ = ("NetBoxLoadBalancingVirtualIPFilter",)


@strawberry_django.filter(VirtualIP, lookups=True)
class NetBoxLoadBalancingVirtualIPFilter(ContactFilterMixin, PrimaryModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    dns_name: FilterLookup[str] | None = strawberry_django.filter_field()
    disabled: FilterLookup[bool] | None = strawberry_django.filter_field()
    virtual_pool: (
        Annotated[
            "NetBoxLoadBalancingVirtualIPPoolFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    virtual_pool_id: ID | None = strawberry_django.filter_field()
    address: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    address_id: ID | None = strawberry_django.filter_field()
    route_health_injection: FilterLookup[bool] | None = strawberry_django.filter_field()
