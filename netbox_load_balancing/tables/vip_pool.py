import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import (
    TagColumn,
    ActionsColumn,
)

from tenancy.tables import TenancyColumnsMixin

from netbox_load_balancing.models import VirtualIPPool, VirtualIPPoolAssignment

__all__ = (
    "VirtualIPPoolTable",
    "VirtualIPPoolAssignmentTable",
)


class VirtualIPPoolTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    disabled = tables.BooleanColumn()
    tags = TagColumn(url_name="plugins:netbox_load_balancing:virtualippool_list")

    class Meta(NetBoxTable.Meta):
        model = VirtualIPPool
        fields = (
            "pk",
            "name",
            "description",
            "tenant",
            "disabled",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "description",
            "tenant",
            "disabled",
            "tags",
        )


class VirtualIPPoolAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Prefix/IP Range"),
    )
    virtual_pool = tables.Column(verbose_name=_("Virtual IP Pool"), linkify=True)
    disabled = tables.BooleanColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = VirtualIPPoolAssignment
        fields = ("pk", "virtual_pool", "assigned_object", "weight", "disabled")
        exclude = ("id",)
