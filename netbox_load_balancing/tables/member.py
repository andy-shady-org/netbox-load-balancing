import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn

from netbox_load_balancing.models import Member, MemberAssignment

__all__ = (
    "MemberTable",
    "MemberAssignmentTable",
)


class MemberTable(NetBoxTable):
    name = tables.LinkColumn()
    ip_address = tables.LinkColumn()
    disabled = tables.BooleanColumn()
    tags = TagColumn(url_name="plugins:netbox_load_balancing:member_list")

    class Meta(NetBoxTable.Meta):
        model = Member
        fields = (
            "pk",
            "name",
            "ip_address",
            "description",
            "reference",
            "disabled",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "ip_address",
            "description",
            "reference",
            "disabled",
            "tags",
        )


class MemberAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Pool/Health Monitor"),
    )
    member = tables.Column(verbose_name=_("Member"), linkify=True)
    disabled = tables.BooleanColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = MemberAssignment
        fields = ("pk", "member", "assigned_object", "weight", "disabled")
        exclude = ("id",)
