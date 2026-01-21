import strawberry

from netbox_load_balancing.choices import (
    HealthMonitorTypeChoices,
    HealthMonitorHTTPVersionChoices,
    PoolAlgorythmChoices,
    PoolSessionPersistenceChoices,
    PoolBackupSessionPersistenceChoices,
    ListenerProtocolChoices,
)

__all__ = (
    "NetBoxLoadBalancingHealthMonitorTypeEnum",
    "NetBoxLoadBalancingHealthMonitorHTTPVersionEnum",
    "NetBoxLoadBalancingPoolAlgorythmEnum",
    "NetBoxLoadBalancingPoolSessionPersistenceEnum",
    "NetBoxLoadBalancingPoolBackupSessionPersistenceEnum",
    "NetBoxLoadBalancingListenerProtocolEnum",
)


NetBoxLoadBalancingHealthMonitorTypeEnum = strawberry.enum(
    HealthMonitorTypeChoices.as_enum()
)
NetBoxLoadBalancingHealthMonitorHTTPVersionEnum = strawberry.enum(
    HealthMonitorHTTPVersionChoices.as_enum()
)
NetBoxLoadBalancingPoolAlgorythmEnum = strawberry.enum(PoolAlgorythmChoices.as_enum())
NetBoxLoadBalancingPoolSessionPersistenceEnum = strawberry.enum(
    PoolSessionPersistenceChoices.as_enum()
)
NetBoxLoadBalancingPoolBackupSessionPersistenceEnum = strawberry.enum(
    PoolBackupSessionPersistenceChoices.as_enum()
)
NetBoxLoadBalancingListenerProtocolEnum = strawberry.enum(
    ListenerProtocolChoices.as_enum()
)
