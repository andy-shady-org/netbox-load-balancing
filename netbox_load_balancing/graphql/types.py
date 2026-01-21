from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType
from ipam.graphql.types import IPAddressType
from tenancy.graphql.types import TenantType

from netbox_load_balancing.models import (
    LBService,
    Listener,
    HealthMonitor,
    Pool,
    Member,
    VirtualIPPool,
    VirtualIP,
)

from .filters import (
    NetBoxLoadBalancingLBServiceFilter,
    NetBoxLoadBalancingListenerFilter,
    NetBoxLoadBalancingHealthMonitorFilter,
    NetBoxLoadBalancingPoolFilter,
    NetBoxLoadBalancingMemberFilter,
    NetBoxLoadBalancingVirtualIPPoolFilter,
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
    max_clients: int
    max_requests: int
    client_timeout: int
    server_timeout: int
    client_keepalive: bool
    surge_protection: bool
    tcp_buffering: bool
    compression: bool


@strawberry_django.type(
    HealthMonitor, fields="__all__", filters=NetBoxLoadBalancingHealthMonitorFilter
)
class NetBoxLoadBalancingHealthMonitorType(PrimaryObjectType):
    name: str
    template: str | None
    type: str
    monitor_url: str | None
    http_response: str | None
    monitor_host: str | None
    http_version: str
    monitor_port: int
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
    name: str
    algorythm: str
    session_persistence: str
    backup_persistence: str
    persistence_timeout: int
    backup_timeout: int
    member_port: int
    disabled: bool


@strawberry_django.type(
    Member, fields="__all__", filters=NetBoxLoadBalancingMemberFilter
)
class NetBoxLoadBalancingMemberType(PrimaryObjectType):
    ip_address: Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")] | None
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
    address: Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")] | None
    name: str
    dns_name: str
    disabled: bool
    route_health_injection: bool
