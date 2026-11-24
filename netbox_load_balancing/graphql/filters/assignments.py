from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin, TenancyFilterMixin
from extras.graphql.filter_mixins import ConfigContextFilterMixin

from netbox_load_balancing.models import (
    HealthMonitorAssignment,
    LBServiceAssignment,
    MemberAssignment,
    PoolAssignment,
    VirtualIPPoolAssignment,
)


@strawberry_django.filter(HealthMonitorAssignment, lookups=True)
class NetBoxLoadBalancingHealthMonitorAssignmentsFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter, ConfigContextFilterMixin
):
    monitor: (
        Annotated[
            "NetBoxLoadBalancingHealthMonitorFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    assigned_object: (
        Annotated[
            "NetBoxLoadBalancingPoolFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(LBServiceAssignment, lookups=True)
class NetBoxLoadBalancingLBServiceAssignmentFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter, ConfigContextFilterMixin
):
    service: (
        Annotated[
            "NetBoxLoadBalancingLBServiceFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    assigned_object: (
        Annotated[
            "NetBoxLoadBalancingVirtualIPFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(MemberAssignment, lookups=True)
class NetBoxLoadBalancingMemberAssignmentFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter, ConfigContextFilterMixin
):
    member: (
        Annotated[
            "NetBoxLoadBalancingMemberFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    assigned_object: (
        Annotated[
            "NetBoxLoadBalancingPoolFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(PoolAssignment, lookups=True)
class NetBoxLoadBalancingPoolAssignmentFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter, ConfigContextFilterMixin
):
    pool: (
        Annotated[
            "NetBoxLoadBalancingHealthMonitorFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    assigned_object: (
        Annotated[
            "NetBoxLoadBalancingLBServiceFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()


@strawberry_django.filter(VirtualIPPoolAssignment, lookups=True)
class NetBoxLoadBalancingVirtualIPPoolAssignmentFilter(
    ContactFilterMixin, TenancyFilterMixin, PrimaryModelFilter, ConfigContextFilterMixin
):
    virtual_pool: (
        Annotated[
            "NetBoxLoadBalancingVirtualIPPoolFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    assigned_object: (
        Annotated[
            "PrefixFilter",
            strawberry.lazy("ipam.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
