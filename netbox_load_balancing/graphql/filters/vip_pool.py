import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin

from netbox_load_balancing.models import (
    VirtualIPPool,
)

__all__ = ("NetBoxLoadBalancingVirtualIPPoolFilter",)


@strawberry_django.filter(VirtualIPPool, lookups=True)
class NetBoxLoadBalancingVirtualIPPoolFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter
):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    disabled: FilterLookup[bool] | None = strawberry_django.filter_field()
