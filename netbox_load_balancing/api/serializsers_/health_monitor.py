from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    JSONField,
    BooleanField,
    IntegerField,
    ListField,
)
from drf_spectacular.utils import extend_schema_field
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer, PrimaryModelSerializer
from utilities.api import get_serializer_for_model

from netbox_load_balancing.models import HealthMonitor, HealthMonitorAssignment


class HealthMonitorSerializer(PrimaryModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_load_balancing-api:healthmonitor-detail"
    )
    monitor_port = IntegerField(
        required=True, validators=[MinValueValidator(1), MaxValueValidator(65534)]
    )
    http_response_codes = ListField(
        child=IntegerField(),
        required=False,
        allow_empty=True,
        default=[],
    )
    probe_interval = IntegerField(required=False)
    response_timeout = IntegerField(required=False)
    disabled = BooleanField(required=False, default=False)

    class Meta:
        model = HealthMonitor
        fields = (
            "id",
            "url",
            "display",
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
            "disabled",
            "type",
            "url",
            "name",
        )


class HealthMonitorAssignmentSerializer(NetBoxModelSerializer):
    monitor = HealthMonitorSerializer(nested=True, required=True, allow_null=False)
    disabled = BooleanField(required=False, default=False)
    weight = IntegerField(required=False, allow_null=True)
    assigned_object_type = ContentTypeField(queryset=ContentType.objects.all())
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = HealthMonitorAssignment
        fields = [
            "id",
            "url",
            "display",
            "monitor",
            "weight",
            "disabled",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
            "created",
            "last_updated",
        ]
        brief_fields = (
            "id",
            "url",
            "display",
            "monitor",
            "weight",
            "disabled",
            "assigned_object_type",
            "assigned_object_id",
        )

    @extend_schema_field(JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, nested=True, context=context).data
