from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    BooleanField,
    CharField,
    ValidationError,
)
from netbox.api.serializers import PrimaryModelSerializer
from ipam.api.serializers import IPAddressSerializer

from ipam.models import IPAddress
from netbox_load_balancing.api.serializers import VirtualIPPoolSerializer
from netbox_load_balancing.models import VirtualIP, VirtualIPPool


class VirtualIPSerializer(PrimaryModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_load_balancing-api:virtualip-detail"
    )
    dns_name = CharField(required=False)
    virtual_pool = VirtualIPPoolSerializer(nested=True, required=True, allow_null=False)
    address = IPAddressSerializer(nested=True, required=False, allow_null=True)
    disabled = BooleanField(required=False, default=False)
    route_health_injection = BooleanField(required=False, default=False)

    class Meta:
        model = VirtualIP
        fields = (
            "id",
            "url",
            "display",
            "name",
            "dns_name",
            "virtual_pool",
            "address",
            "disabled",
            "route_health_injection",
            "description",
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
            "dns_name",
            "route_health_injection",
        )

    def validate(self, data):
        error_message = {}
        if isinstance(data, dict):
            if (virtual_pool := data.get("virtual_pool")) is not None:
                try:
                    virtual_pool = VirtualIPPool.objects.get(name=virtual_pool)
                except ObjectDoesNotExist:
                    error_message["virtual_pool"] = ["Virtual Pool does not exist"]
                    raise ValidationError(error_message)

                if (address := data.get("address")) is not None:
                    q = virtual_pool.virtualippoolassignment_related.filter(
                        disabled=False
                    )
                    if not q:
                        error_message_virtual_pool = "No Prefixes or IP Ranges have been assigned to this Virtual Pool"
                        error_message["virtual_pool"] = [error_message_virtual_pool]
                        raise ValidationError(error_message)
                    for item in q:
                        if address in item.assigned_object.get_child_ips():
                            return data
                    error_message_address = "Address is not in Prefix or Range associated to this Virtual Pool"
                    error_message["address"] = [error_message_address]
                else:
                    q = virtual_pool.virtualippoolassignment_related.filter(
                        disabled=False
                    ).order_by("weight")
                    if not q:
                        error_message_virtual_pool = "No Prefixes or IP Ranges have been assigned to this Virtual Pool"
                        error_message["virtual_pool"] = [error_message_virtual_pool]
                    else:
                        for item in q:
                            if (
                                hasattr(item.assigned_object, "first_available_ip")
                                and item.assigned_object.first_available_ip
                            ):
                                address = IPAddress.objects.create(
                                    address=item.assigned_object.first_available_ip,
                                    status="active",
                                    dns_name=data.get("dns_name"),
                                    vrf=item.assigned_object.vrf,
                                    tenant_id=item.assigned_object.tenant,
                                )
                                data["address"] = address
                            elif (
                                hasattr(item.assigned_object, "get_first_available_ip")
                                and item.assigned_object.get_first_available_ip()
                            ):
                                address = IPAddress.objects.create(
                                    address=item.assigned_object.get_first_available_ip(),
                                    status="active",
                                    dns_name=data.get("dns_name"),
                                    vrf=item.assigned_object.vrf,
                                    tenant_id=item.assigned_object.tenant,
                                )
                                data["address"] = address
                            else:
                                continue
                    if data.get("address") is None:
                        error_message_address = (
                            "No free IP addresses assigned to this Virtual Pool"
                        )
                        error_message["address"] = [error_message_address]
        if error_message:
            raise ValidationError(error_message)
        return super().validate(data)
