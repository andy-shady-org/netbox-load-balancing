import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ActionsColumn, ManyToManyColumn

from netbox_load_balancing.models import Pool, PoolAssignment

__all__ = (
    "PoolTable",
    "PoolAssignmentTable",
)


class PoolTable(NetBoxTable):
    name = tables.LinkColumn()
    listeners = ManyToManyColumn()
    disabled = tables.BooleanColumn()
    tags = TagColumn(url_name="plugins:netbox_load_balancing:pool_list")

    class Meta(NetBoxTable.Meta):
        model = Pool
        fields = (
            "pk",
            "name",
            "listeners",
            "description",
            "algorythm",
            "session_persistence",
            "backup_persistence",
            "persistence_timeout",
            "backup_timeout",
            "member_port",
            "disabled",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "description",
            "algorythm",
            "session_persistence",
            "persistence_timeout",
            "member_port",
            "disabled",
            "tags",
        )


class PoolAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("LB Service"),
    )
    pool = tables.Column(verbose_name=_("Pool"), linkify=True)
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = PoolAssignment
        fields = ("pk", "pool", "assigned_object")
        exclude = ("id",)
