import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import (
    TagColumn,
    ActionsColumn,
    ChoiceFieldColumn,
    ArrayColumn,
)

from netbox_load_balancing.models import HealthMonitor, HealthMonitorAssignment

__all__ = (
    "HealthMonitorTable",
    "HealthMonitorAssignmentTable",
)


class HealthMonitorTable(NetBoxTable):
    name = tables.LinkColumn()
    type = ChoiceFieldColumn()
    http_version = ChoiceFieldColumn()
    http_secure = tables.BooleanColumn()
    http_response_codes = ArrayColumn()
    disabled = tables.BooleanColumn()
    tags = TagColumn(url_name="plugins:netbox_load_balancing:healthmonitor_list")

    class Meta(NetBoxTable.Meta):
        model = HealthMonitor
        fields = (
            "pk",
            "name",
            "description",
            "template",
            "type",
            "monitor_url",
            "http_response",
            "monitor_host",
            "monitor_port",
            "http_version",
            "http_secure",
            "http_response_codes",
            "probe_interval",
            "response_timeout",
            "disabled",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "description",
            "template",
            "type",
            "monitor_url",
            "monitor_host",
            "monitor_port",
            "http_version",
            "http_secure",
            "disabled",
            "tags",
        )


class HealthMonitorAssignmentTable(NetBoxTable):
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_("Pool"),
    )
    monitor = tables.Column(verbose_name=_("Health Monitor"), linkify=True)
    disabled = tables.BooleanColumn()
    actions = ActionsColumn(actions=("edit", "delete"))

    class Meta(NetBoxTable.Meta):
        model = HealthMonitorAssignment
        fields = ("pk", "monitor", "assigned_object", "weight", "disabled")
        exclude = ("id",)
