from rest_framework.serializers import (
    HyperlinkedIdentityField,
    BooleanField,
    IntegerField,
)
from netbox.api.serializers import PrimaryModelSerializer

from netbox_load_balancing.api.serializers import LBServiceSerializer
from netbox_load_balancing.models import Listener
from netbox_load_balancing.choices import ListenerProtocolChoices


class ListenerSerializer(PrimaryModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_load_balancing-api:listener-detail"
    )
    service = LBServiceSerializer(nested=True, required=True, many=False)
    port = IntegerField(required=True)
    max_clients = IntegerField(required=False, default=0)
    max_requests = IntegerField(required=False, default=0)
    client_timeout = IntegerField(required=False, default=9000)
    server_timeout = IntegerField(required=False, default=9000)
    source_nat = BooleanField(required=False, default=True)
    use_proxy_port = BooleanField(required=False, default=False)
    client_keepalive = BooleanField(required=False, default=False)
    surge_protection = BooleanField(required=False, default=False)
    tcp_buffering = BooleanField(required=False, default=False)
    compression = BooleanField(required=False, default=False)

    class Meta:
        model = Listener
        fields = (
            "id",
            "url",
            "display",
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
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "description",
            "display",
            "name",
            "port",
        )
