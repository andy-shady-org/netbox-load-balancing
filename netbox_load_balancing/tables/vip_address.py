import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn
from tenancy.tables import TenancyColumnsMixin

from netbox_load_balancing.models import VirtualIP

__all__ = ("VirtualIPTable",)


class VirtualIPTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.LinkColumn()
    dns_name = tables.Column()
    virtual_pool = tables.LinkColumn()
    address = tables.LinkColumn()
    disabled = tables.BooleanColumn()
    route_health_injection = tables.BooleanColumn()
    tags = TagColumn(url_name="plugins:netbox_load_balancing:virtualip_list")

    class Meta(NetBoxTable.Meta):
        model = VirtualIP
        fields = (
            "pk",
            "name",
            "dns_name",
            "description",
            "virtual_pool",
            "address",
            "disabled",
            "route_health_injection",
            "tenant",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "dns_name",
            "description",
            "virtual_pool",
            "address",
            "disabled",
            "route_health_injection",
            "tenant",
            "tags",
        )
