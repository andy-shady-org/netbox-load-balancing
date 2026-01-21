from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    JSONField,
    BooleanField,
    IntegerField,
)
from drf_spectacular.utils import extend_schema_field
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer, PrimaryModelSerializer
from utilities.api import get_serializer_for_model
from tenancy.api.serializers import TenantSerializer

from netbox_load_balancing.models import VirtualIPPool, VirtualIPPoolAssignment


class VirtualIPPoolSerializer(PrimaryModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_load_balancing-api:virtualippool-detail"
    )
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    disabled = BooleanField(required=False, default=False)

    class Meta:
        model = VirtualIPPool
        fields = (
            "id",
            "url",
            "display",
            "name",
            "disabled",
            "description",
            "tenant",
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
            "name",
        )


class VirtualIPPoolAssignmentSerializer(NetBoxModelSerializer):
    virtual_pool = VirtualIPPoolSerializer(nested=True, required=True, allow_null=False)
    disabled = BooleanField(required=False, default=False)
    weight = IntegerField(required=False, allow_null=True)
    assigned_object_type = ContentTypeField(queryset=ContentType.objects.all())
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = VirtualIPPoolAssignment
        fields = [
            "id",
            "url",
            "display",
            "virtual_pool",
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
            "virtual_pool",
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
