from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from tenancy.graphql.filter_mixins import ContactFilterMixin
from netbox_load_balancing.graphql.enums import (
    NetBoxLoadBalancingPoolAlgorythmEnum,
    NetBoxLoadBalancingPoolSessionPersistenceEnum,
    NetBoxLoadBalancingPoolBackupSessionPersistenceEnum,
)

from netbox_load_balancing.models import (
    Pool,
)
from netbox_load_balancing.graphql.filters import NetBoxLoadBalancingListenerFilter

__all__ = ("NetBoxLoadBalancingPoolFilter",)


@strawberry_django.filter(Pool, lookups=True)
class NetBoxLoadBalancingPoolFilter(ContactFilterMixin, PrimaryModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
    listeners: (
        Annotated[
            "NetBoxLoadBalancingListenerFilter",
            strawberry.lazy("netbox_load_balancing.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    algorythm: (
        Annotated[
            "NetBoxLoadBalancingPoolAlgorythmEnum",
            strawberry.lazy("netbox_load_balancing.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    session_persistence: (
        Annotated[
            "NetBoxLoadBalancingPoolSessionPersistenceEnum",
            strawberry.lazy("netbox_load_balancing.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    backup_persistence: (
        Annotated[
            "NetBoxLoadBalancingPoolBackupSessionPersistenceEnum",
            strawberry.lazy("netbox_load_balancing.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()
    persistence_timeout: FilterLookup[int] | None = strawberry_django.filter_field()
    backup_timeout: FilterLookup[int] | None = strawberry_django.filter_field()
    member_port: FilterLookup[int] | None = strawberry_django.filter_field()
    disabled: FilterLookup[bool] | None = strawberry_django.filter_field()
