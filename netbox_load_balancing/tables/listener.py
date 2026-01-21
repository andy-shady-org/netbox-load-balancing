import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn

from netbox_load_balancing.models import Listener

__all__ = ("ListenerTable",)


class ListenerTable(NetBoxTable):
    name = tables.LinkColumn()
    service = tables.LinkColumn()
    source_nat = tables.BooleanColumn()
    use_proxy_port = tables.BooleanColumn()
    client_keepalive = tables.BooleanColumn()
    surge_protection = tables.BooleanColumn()
    tcp_buffering = tables.BooleanColumn()
    compression = tables.BooleanColumn()
    tags = TagColumn(url_name="plugins:netbox_load_balancing:listener_list")

    class Meta(NetBoxTable.Meta):
        model = Listener
        fields = (
            "pk",
            "name",
            "service",
            "description",
            "port",
            "protocol",
            "source_nat",
            "use_proxy_port",
            "max_clients",
            "max_requests",
            "client_timeout",
            "server_timeout",
            "client_keepalive",
            "surge_protection",
            "tcp_buffering",
            "compression",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "service",
            "description",
            "port",
            "protocol",
            "tags",
        )
