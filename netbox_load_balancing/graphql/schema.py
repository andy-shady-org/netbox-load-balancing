from typing import List

import strawberry
import strawberry_django

from .types import (
    NetBoxLoadBalancingLBServiceType,
    NetBoxLoadBalancingLBServiceAssignmentType,
    NetBoxLoadBalancingListenerType,
    NetBoxLoadBalancingPoolType,
    NetBoxLoadBalancingPoolAssignmentType,
    NetBoxLoadBalancingMemberType,
    NetBoxLoadBalancingMemberAssignmentType,
    NetBoxLoadBalancingHealthMonitorType,
    NetBoxLoadBalancingHealthMonitorAssignmentType,
    NetBoxLoadBalancingVirtualIPPoolType,
    NetBoxLoadBalancingVirtualIPPoolAssignmentType,
    NetBoxLoadBalancingVirtualIPType,
)


@strawberry.type(name="Query")
class NetBoxLoadBalancingLBServiceQuery:
    netbox_load_balancing_lbservice: NetBoxLoadBalancingLBServiceType = (
        strawberry_django.field()
    )
    netbox_load_balancing_lbservice_list: List[NetBoxLoadBalancingLBServiceType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxLoadBalancingListenerQuery:
    netbox_load_balancing_listener: NetBoxLoadBalancingListenerType = (
        strawberry_django.field()
    )
    netbox_load_balancing_listener_list: List[NetBoxLoadBalancingListenerType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxLoadBalancingPoolQuery:
    netbox_load_balancing_pool: NetBoxLoadBalancingPoolType = strawberry_django.field()
    netbox_load_balancing_pool_list: List[NetBoxLoadBalancingPoolType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxLoadBalancingMemberQuery:
    netbox_load_balancing_member: NetBoxLoadBalancingMemberType = (
        strawberry_django.field()
    )
    netbox_load_balancing_member_list: List[NetBoxLoadBalancingMemberType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxLoadBalancingHealthMonitorQuery:
    netbox_load_balancing_healthmonitor: NetBoxLoadBalancingHealthMonitorType = (
        strawberry_django.field()
    )
    netbox_load_balancing_healthmonitor_list: List[
        NetBoxLoadBalancingHealthMonitorType
    ] = strawberry_django.field()


@strawberry.type(name="Query")
class NetBoxLoadBalancingVirtualIPPoolQuery:
    netbox_load_balancing_virtualippool: NetBoxLoadBalancingVirtualIPPoolType = (
        strawberry_django.field()
    )
    netbox_load_balancing_virtualippool_list: List[
        NetBoxLoadBalancingVirtualIPPoolType
    ] = strawberry_django.field()


@strawberry.type(name="Query")
class NetBoxLoadBalancingVirtualIPQuery:
    netbox_load_balancing_virtualip: NetBoxLoadBalancingVirtualIPType = (
        strawberry_django.field()
    )
    netbox_load_balancing_virtualip_list: List[NetBoxLoadBalancingVirtualIPType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxLoadBalancingHealthMonitorAssignmentQuery:
    netbox_load_balancing_healthmonitor_assignments: List[
        NetBoxLoadBalancingHealthMonitorAssignmentType
    ] = strawberry_django.field()


@strawberry.type(name="Query")
class NetBoxLoadBalancingLBServiceAssignmentQuery:
    netbox_load_balancing_lbservice_assignments: List[
        NetBoxLoadBalancingLBServiceAssignmentType
    ] = strawberry_django.field()


@strawberry.type(name="Query")
class NetBoxLoadBalancingMemberAssignmentQuery:
    netbox_load_balancing_member_assignments: List[
        NetBoxLoadBalancingMemberAssignmentType
    ] = strawberry_django.field()


@strawberry.type(name="Query")
class NetBoxLoadBalancingPoolAssignmentQuery:
    netbox_load_balancing_pool_assignments: List[
        NetBoxLoadBalancingPoolAssignmentType
    ] = strawberry_django.field()


@strawberry.type(name="Query")
class NetBoxLoadBalancingVirtualIPPoolAssignmentQuery:
    netbox_load_balancing_virtualippool_assignments: List[
        NetBoxLoadBalancingVirtualIPPoolAssignmentType
    ] = strawberry_django.field()
