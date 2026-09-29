from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup
from strawberry.scalars import ID

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin
from ipam.graphql.filters import IPAddressFilter
from extras.graphql.filter_mixins import ConfigContextFilterMixin

from netbox_load_balancing.models import (
    Member,
)

__all__ = ("NetBoxLoadBalancingMemberFilter",)


@strawberry_django.filter(Member, lookups=True)
class NetBoxLoadBalancingMemberFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter, ConfigContextFilterMixin
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
    reference: StrFilterLookup[str] | None = strawberry_django.filter_field()
    ip_address: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    ip_address_id: ID | None = strawberry_django.filter_field()
    disabled: FilterLookup[bool] | None = strawberry_django.filter_field()
