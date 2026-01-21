import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_load_balancing.models import LBService, LBServiceAssignment

__all__ = (
    "LBServiceTable",
    "LBServiceAssignmentTable",
)


class LBServiceTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    disabled = tables.BooleanColumn()
    tags = TagColumn(url_name="plugins:netbox_load_balancing:service_list")

    class Meta(NetBoxTable.Meta):
        model = LBService
        fields = (
            "pk",
            "name",
            "description",
            "reference",
            "disabled",
            "tenant",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "description",
            "reference",
            "disabled",
            "tenant",
            "tags",
        )


class LBServiceAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("IP Address"),
    )
    service = tables.Column(verbose_name=_("LBService"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = LBServiceAssignment
        fields = ("pk", "service", "assigned_object")
        exclude = ("id",)
