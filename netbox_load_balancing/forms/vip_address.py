from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelBulkEditForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelForm,
)

from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    DynamicModelChoiceField,
    TagFilterField,
    CommentField,
    CSVModelChoiceField,
    DynamicModelMultipleChoiceField,
)

from ipam.models import IPAddress

from netbox_load_balancing.models import (
    VirtualIP,
    VirtualIPPool,
)

__all__ = (
    "VirtualIPForm",
    "VirtualIPFilterForm",
    "VirtualIPImportForm",
    "VirtualIPBulkEditForm",
)


class VirtualIPForm(PrimaryModelForm):
    name = forms.CharField(max_length=255, required=True)
    dns_name = forms.CharField(max_length=255, required=False, label=_("DNS name"))
    virtual_pool = DynamicModelChoiceField(
        queryset=VirtualIPPool.objects.all(),
        required=True,
    )
    address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
    )
    description = forms.CharField(max_length=200, required=False)
    disabled = forms.BooleanField(required=False)
    route_health_injection = forms.BooleanField(required=False)
    fieldsets = (
        FieldSet(
            "name",
            "dns_name",
            "virtual_pool",
            "address",
            "description",
            "disabled",
            name=_("Virtual IP"),
        ),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = VirtualIP
        fields = [
            "name",
            "owner",
            "dns_name",
            "route_health_injection",
            "description",
            "disabled",
            "address",
            "virtual_pool",
            "comments",
            "tags",
        ]

    def clean(self):
        super().clean()
        error_message = {}
        if (virtual_pool := self.cleaned_data.get("virtual_pool")) is not None:
            try:
                virtual_pool = VirtualIPPool.objects.get(name=virtual_pool)
            except ObjectDoesNotExist:
                error_message["virtual_pool"] = ["Virtual Pool does not exist"]
                raise forms.ValidationError(error_message)

            if (address := self.cleaned_data.get("address")) is not None:
                q = virtual_pool.virtualippoolassignment_related.filter(disabled=False)
                if not q:
                    error_message_virtual_pool = "No Prefixes or IP Ranges have been assigned to this Virtual Pool"
                    error_message["virtual_pool"] = [error_message_virtual_pool]
                    raise forms.ValidationError(error_message)
                for item in q:
                    if address in item.assigned_object.get_child_ips():
                        return self.cleaned_data
                error_message_address = (
                    "Address is not in Prefix or Range associated to this Virtual Pool"
                )
                error_message["address"] = [error_message_address]
                raise forms.ValidationError(error_message)
            else:
                if virtual_pool.disabled:
                    error_message["virtual_pool"] = [
                        "Virtual Pool is disabled and cannot be used to allocate new VIP Addresses"
                    ]
                    raise forms.ValidationError(error_message)

                q = virtual_pool.virtualippoolassignment_related.filter(
                    disabled=False
                ).order_by("weight")
                if not q:
                    error_message_virtual_pool = "No Prefixes or IP Ranges have been assigned to this Virtual Pool"
                    error_message["virtual_pool"] = [error_message_virtual_pool]
                    raise forms.ValidationError(error_message)
                for item in q:
                    if (
                        hasattr(item.assigned_object, "first_available_ip")
                        and item.assigned_object.first_available_ip
                    ):
                        address = IPAddress.objects.create(
                            address=item.assigned_object.first_available_ip,
                            status="active",
                            dns_name=self.cleaned_data.get("dns_name"),
                            vrf=item.assigned_object.vrf,
                            tenant_id=item.assigned_object.tenant,
                        )
                        self.cleaned_data["address"] = address
                    elif (
                        hasattr(item.assigned_object, "get_first_available_ip")
                        and item.assigned_object.get_first_available_ip()
                    ):
                        address = IPAddress.objects.create(
                            address=item.assigned_object.get_first_available_ip(),
                            status="active",
                            dns_name=self.cleaned_data.get("dns_name"),
                            vrf=item.assigned_object.vrf,
                            tenant_id=item.assigned_object.tenant,
                        )
                        self.cleaned_data["address"] = address
                    else:
                        continue
                if self.cleaned_data.get("address") is None:
                    error_message_address = (
                        "No free IP addresses assigned to this Virtual Pool"
                    )
                    error_message["address"] = [error_message_address]
                    raise forms.ValidationError(error_message)
        return self.cleaned_data


class VirtualIPFilterForm(PrimaryModelFilterSetForm):
    model = VirtualIP
    fieldsets = (
        FieldSet("q", "filter_id", "tag", "owner_id"),
        FieldSet(
            "name",
            "dns_name",
            "virtual_pool",
            "address",
            "disabled",
            "route_health_injection",
            name=_("Virtual IP"),
        ),
    )
    virtual_pool = DynamicModelMultipleChoiceField(
        queryset=VirtualIPPool.objects.all(),
        required=False,
    )
    address = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
    )
    disabled = forms.BooleanField(required=False)
    route_health_injection = forms.BooleanField(required=False)
    tags = TagFilterField(model)


class VirtualIPImportForm(PrimaryModelImportForm):
    name = forms.CharField(max_length=255, required=True)
    dns_name = forms.CharField(max_length=255, required=False, label=_("DNS name"))
    virtual_pool = CSVModelChoiceField(
        queryset=VirtualIPPool.objects.all(),
        required=True,
        to_field_name="name",
        help_text=_("Virtual Pool (Name)"),
    )
    address = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        to_field_name="address",
        help_text=_("IP Address (address)"),
    )
    disabled = forms.BooleanField(required=False)
    route_health_injection = forms.BooleanField(required=False)

    class Meta:
        model = VirtualIP
        fields = (
            "name",
            "owner",
            "dns_name",
            "address",
            "virtual_pool",
            "description",
            "disabled",
            "route_health_injection",
            "tags",
        )

    def clean(self):
        super().clean()
        error_message = {}
        if (virtual_pool := self.cleaned_data.get("virtual_pool")) is not None:
            try:
                virtual_pool = VirtualIPPool.objects.get(name=virtual_pool)
            except ObjectDoesNotExist:
                error_message["virtual_pool"] = ["Virtual Pool does not exist"]
                raise forms.ValidationError(error_message)

            if (address := self.cleaned_data.get("address")) is not None:
                q = virtual_pool.virtualippoolassignment_related.filter(disabled=False)
                if not q:
                    error_message_virtual_pool = "No Prefixes or IP Ranges have been assigned to this Virtual Pool"
                    error_message["virtual_pool"] = [error_message_virtual_pool]
                    raise forms.ValidationError(error_message)
                for item in q:
                    if address in item.assigned_object.get_child_ips():
                        return self.cleaned_data
                error_message_address = (
                    "Address is not in Prefix or Range associated to this Virtual Pool"
                )
                error_message["address"] = [error_message_address]
                raise forms.ValidationError(error_message)
            else:
                if virtual_pool.disabled:
                    error_message["virtual_pool"] = [
                        "Virtual Pool is disabled and cannot be used to allocate new VIP Addresses"
                    ]
                    raise forms.ValidationError(error_message)

                q = virtual_pool.virtualippoolassignment_related.filter(
                    disabled=False
                ).order_by("weight")
                if not q:
                    error_message_virtual_pool = "No Prefixes or IP Ranges have been assigned to this Virtual Pool"
                    error_message["virtual_pool"] = [error_message_virtual_pool]
                    raise forms.ValidationError(error_message)
                for item in q:
                    if (
                        hasattr(item.assigned_object, "first_available_ip")
                        and item.assigned_object.first_available_ip
                    ):
                        address = IPAddress.objects.create(
                            address=item.assigned_object.first_available_ip,
                            status="active",
                            dns_name=self.cleaned_data.get("dns_name"),
                        )
                        self.cleaned_data["address"] = address
                    elif (
                        hasattr(item.assigned_object, "get_first_available_ip")
                        and item.assigned_object.get_first_available_ip()
                    ):
                        address = IPAddress.objects.create(
                            address=item.assigned_object.get_first_available_ip(),
                            status="active",
                            dns_name=self.cleaned_data.get("dns_name"),
                        )
                        self.cleaned_data["address"] = address
                    else:
                        continue
                if self.cleaned_data.get("address") is None:
                    error_message_address = (
                        "No free IP addresses assigned to this Virtual Pool"
                    )
                    error_message["address"] = [error_message_address]
                    raise forms.ValidationError(error_message)
        return self.cleaned_data


class VirtualIPBulkEditForm(PrimaryModelBulkEditForm):
    model = VirtualIP
    dns_name = forms.CharField(max_length=255, required=False, label=_("DNS name"))
    description = forms.CharField(max_length=200, required=False)
    disabled = forms.BooleanField(required=False)
    route_health_injection = forms.BooleanField(required=False)
    tags = TagFilterField(model)
    virtual_pool = DynamicModelChoiceField(
        queryset=VirtualIPPool.objects.all(),
        required=False,
        label=_("Virtual Pool"),
    )
    address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label=_("IP Address"),
        # query_params={
        #     'site_id': '$site'
        # }
    )
    nullable_fields = ["description"]
    fieldsets = (
        FieldSet(
            "address",
            "dns_name",
            "virtual_pool",
            "description",
            "disabled",
            "route_health_injection",
            name=_("Virtual IP"),
        ),
        FieldSet("tags", name=_("Tags")),
    )
