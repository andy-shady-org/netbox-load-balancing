from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
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

from netbox_load_balancing.models import Pool, PoolAssignment
from netbox_load_balancing.api.serializers import ListenerSerializer


class PoolSerializer(PrimaryModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_load_balancing-api:pool-detail"
    )
    listeners = ListenerSerializer(nested=True, many=True, required=True)
    disabled = BooleanField(required=False, default=False)
    persistence_timeout = IntegerField(required=False, default=0)
    backup_timeout = IntegerField(required=False, default=0)
    member_port = IntegerField(
        required=False, validators=[MinValueValidator(1), MaxValueValidator(65535)]
    )

    class Meta:
        model = Pool
        fields = (
            "id",
            "url",
            "display",
            "name",
            "disabled",
            "description",
            "listeners",
            "algorythm",
            "session_persistence",
            "backup_persistence",
            "persistence_timeout",
            "backup_timeout",
            "member_port",
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

    def create(self, validated_data):
        listeners = validated_data.pop("listeners", None)
        pool = super().create(validated_data)
        if listeners is not None:
            pool.listeners.set(listeners)
        return pool

    def update(self, instance, validated_data):
        listeners = validated_data.pop("listeners", None)
        pool = super().update(instance, validated_data)
        if listeners is not None:
            pool.listeners.set(listeners)
        return pool


class PoolAssignmentSerializer(NetBoxModelSerializer):
    pool = PoolSerializer(nested=True, required=True, allow_null=False)
    assigned_object_type = ContentTypeField(queryset=ContentType.objects.all())
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = PoolAssignment
        fields = [
            "id",
            "url",
            "display",
            "pool",
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
            "pool",
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
