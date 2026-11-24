from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType
from ipam.graphql.types import IPAddressType
from tenancy.graphql.types import TenantType

from netbox_load_balancing.models import (
    LBService,
    LBServiceAssignment,
    Listener,
    HealthMonitor,
    HealthMonitorAssignment,
    Pool,
    PoolAssignment,
    Member,
    MemberAssignment,
    VirtualIPPool,
    VirtualIPPoolAssignment,
    VirtualIP,
)

from .filters import (
    NetBoxLoadBalancingLBServiceFilter,
    NetBoxLoadBalancingLBServiceAssignmentFilter,
    NetBoxLoadBalancingListenerFilter,
    NetBoxLoadBalancingHealthMonitorFilter,
    NetBoxLoadBalancingHealthMonitorAssignmentsFilter,
    NetBoxLoadBalancingPoolFilter,
    NetBoxLoadBalancingPoolAssignmentFilter,
    NetBoxLoadBalancingMemberFilter,
    NetBoxLoadBalancingMemberAssignmentFilter,
    NetBoxLoadBalancingVirtualIPPoolFilter,
    NetBoxLoadBalancingVirtualIPPoolAssignmentFilter,
    NetBoxLoadBalancingVirtualIPFilter,
)


@strawberry_django.type(
    LBService, fields="__all__", filters=NetBoxLoadBalancingLBServiceFilter
)
class NetBoxLoadBalancingLBServiceType(PrimaryObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    reference: str
    disabled: bool


@strawberry_django.type(
    Listener, fields="__all__", filters=NetBoxLoadBalancingListenerFilter
)
class NetBoxLoadBalancingListenerType(PrimaryObjectType):
    name: str
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    service: (
        Annotated[
            "NetBoxLoadBalancingLBServiceType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )
    port: int
    protocol: str
    source_nat: bool
    use_proxy_port: bool
    max_clients: int | None
    max_requests: int | None
    client_timeout: int | None
    server_timeout: int | None
    client_keepalive: bool
    surge_protection: bool
    tcp_buffering: bool
    compression: bool


@strawberry_django.type(
    HealthMonitor, fields="__all__", filters=NetBoxLoadBalancingHealthMonitorFilter
)
class NetBoxLoadBalancingHealthMonitorType(PrimaryObjectType):
    name: str
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    template: str | None
    type: str
    monitor_url: str | None
    http_response: str | None
    monitor_host: str | None
    http_version: str
    monitor_port: int | None
    http_secure: bool
    http_response_codes: List[int] | None
    probe_interval: int | None
    response_timeout: int | None
    disabled: bool


@strawberry_django.type(Pool, fields="__all__", filters=NetBoxLoadBalancingPoolFilter)
class NetBoxLoadBalancingPoolType(PrimaryObjectType):
    listeners: (
        List[
            Annotated[
                "NetBoxLoadBalancingListenerType",
                strawberry.lazy("netbox_load_balancing.graphql.types"),
            ]
        ]
        | None
    )
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    algorythm: str
    session_persistence: str
    backup_persistence: str
    persistence_timeout: int | None
    backup_timeout: int | None
    member_port: int | None
    disabled: bool


@strawberry_django.type(
    Member, fields="__all__", filters=NetBoxLoadBalancingMemberFilter
)
class NetBoxLoadBalancingMemberType(PrimaryObjectType):
    ip_address: Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")] | None
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    reference: str
    disabled: bool


@strawberry_django.type(
    VirtualIPPool, fields="__all__", filters=NetBoxLoadBalancingVirtualIPPoolFilter
)
class NetBoxLoadBalancingVirtualIPPoolType(PrimaryObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    disabled: bool


@strawberry_django.type(
    VirtualIP, fields="__all__", filters=NetBoxLoadBalancingVirtualIPFilter
)
class NetBoxLoadBalancingVirtualIPType(PrimaryObjectType):
    virtual_pool: (
        Annotated[
            "NetBoxLoadBalancingVirtualIPPoolType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    address: Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")] | None
    name: str
    dns_name: str
    disabled: bool
    route_health_injection: bool


@strawberry_django.type(
    HealthMonitorAssignment,
    fields="__all__",
    filters=NetBoxLoadBalancingHealthMonitorAssignmentsFilter,
)
class NetBoxLoadBalancingHealthMonitorAssignmentType(PrimaryObjectType):
    monitor: (
        Annotated[
            "NetBoxLoadBalancingHealthMonitorType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )
    assigned_object: (
        Annotated[
            "NetBoxLoadBalancingPoolType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )


@strawberry_django.type(
    LBServiceAssignment,
    fields="__all__",
    filters=NetBoxLoadBalancingLBServiceAssignmentFilter,
)
class NetBoxLoadBalancingLBServiceAssignmentType(PrimaryObjectType):
    service: (
        Annotated[
            "NetBoxLoadBalancingLBServiceType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )
    assigned_object: (
        Annotated[
            "NetBoxLoadBalancingVirtualIPType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )


@strawberry_django.type(
    MemberAssignment,
    fields="__all__",
    filters=NetBoxLoadBalancingMemberAssignmentFilter,
)
class NetBoxLoadBalancingMemberAssignmentType(PrimaryObjectType):
    member: (
        Annotated[
            "NetBoxLoadBalancingMemberType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )
    assigned_object: (
        Annotated[
            "NetBoxLoadBalancingPoolType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )


@strawberry_django.type(
    PoolAssignment, fields="__all__", filters=NetBoxLoadBalancingPoolAssignmentFilter
)
class NetBoxLoadBalancingPoolAssignmentType(PrimaryObjectType):
    pool: (
        Annotated[
            "NetBoxLoadBalancingPoolType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )
    assigned_object: (
        Annotated[
            "NetBoxLoadBalancingLBServiceType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )


@strawberry_django.type(
    VirtualIPPoolAssignment,
    fields="__all__",
    filters=NetBoxLoadBalancingVirtualIPPoolAssignmentFilter,
)
class NetBoxLoadBalancingVirtualIPPoolAssignmentType(PrimaryObjectType):
    virtual_pool: (
        Annotated[
            "NetBoxLoadBalancingVirtualIPPoolType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )
    assigned_object: (
        Annotated[
            "PrefixType",
            strawberry.lazy("ipam.graphql.types"),
        ]
        | None
    )
