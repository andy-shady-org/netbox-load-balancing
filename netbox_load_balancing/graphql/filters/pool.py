from typing import Annotated
import strawberry
import strawberry_django
from strawberry_django import FilterLookup

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filter_lookups import IntegerLookup

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
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    description: StrFilterLookup[str] | None = strawberry_django.filter_field()
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
    persistence_timeout: (
        Annotated["IntegerLookup", strawberry.lazy("netbox.graphql.filter_lookups")]
        | None
    ) = strawberry_django.filter_field()
    backup_timeout: (
        Annotated["IntegerLookup", strawberry.lazy("netbox.graphql.filter_lookups")]
        | None
    ) = strawberry_django.filter_field()
    member_port: (
        Annotated["IntegerLookup", strawberry.lazy("netbox.graphql.filter_lookups")]
        | None
    ) = strawberry_django.filter_field()
    disabled: FilterLookup[bool] | None = strawberry_django.filter_field()
