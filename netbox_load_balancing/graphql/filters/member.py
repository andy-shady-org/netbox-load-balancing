from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup
from strawberry.scalars import ID

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin
from ipam.graphql.filters import IPAddressFilter

from netbox_load_balancing.models import (
    Member,
)

__all__ = ("NetBoxLoadBalancingMemberFilter",)


@strawberry_django.filter(Member, lookups=True)
class NetBoxLoadBalancingMemberFilter(ContactFilterMixin, PrimaryModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    reference: FilterLookup[str] | None = strawberry_django.filter_field()
    ip_address: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    ip_address_id: ID | None = strawberry_django.filter_field()
    disabled: FilterLookup[bool] | None = strawberry_django.filter_field()
