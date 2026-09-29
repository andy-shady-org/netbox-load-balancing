import strawberry_django
from strawberry_django import FilterLookup

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin
from extras.graphql.filter_mixins import ConfigContextFilterMixin

from netbox_load_balancing.models import (
    VirtualIPPool,
)

__all__ = ("NetBoxLoadBalancingVirtualIPPoolFilter",)


@strawberry_django.filter(VirtualIPPool, lookups=True)
class NetBoxLoadBalancingVirtualIPPoolFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter, ConfigContextFilterMixin
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    disabled: FilterLookup[bool] | None = strawberry_django.filter_field()
