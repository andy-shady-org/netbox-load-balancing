from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelBulkEditForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelForm,
)

from tenancy.forms import TenancyForm, TenancyFilterForm
from utilities.forms.rendering import FieldSet, ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
    TagFilterField,
    CommentField,
    CSVModelChoiceField,
)

from tenancy.models import Tenant, TenantGroup

from netbox_load_balancing.models import (
    VirtualIPPool,
    VirtualIPPoolAssignment,
)

__all__ = (
    "VirtualIPPoolForm",
    "VirtualIPPoolFilterForm",
    "VirtualIPPoolImportForm",
    "VirtualIPPoolBulkEditForm",
    "VirtualIPPoolAssignmentForm",
)


class VirtualIPPoolForm(TenancyForm, PrimaryModelForm):
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(max_length=200, required=False)
    disabled = forms.BooleanField(required=False)
    fieldsets = (
        FieldSet("name", "description", "disabled", name=_("Virtual IP Pool")),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = VirtualIPPool
        fields = [
            "name",
            "owner",
            "description",
            "disabled",
            "tenant_group",
            "tenant",
            "comments",
            "tags",
        ]


class VirtualIPPoolFilterForm(TenancyFilterForm, PrimaryModelFilterSetForm):
    model = VirtualIPPool
    fieldsets = (
        FieldSet("q", "filter_id", "tag", "owner_id"),
        FieldSet("name", name=_("Virtual IP Pool")),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    tags = TagFilterField(model)


class VirtualIPPoolImportForm(PrimaryModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Tenant"),
    )

    class Meta:
        model = VirtualIPPool
        fields = (
            "name",
            "owner",
            "description",
            "disabled",
            "tenant",
            "tags",
        )


class VirtualIPPoolBulkEditForm(PrimaryModelBulkEditForm):
    model = VirtualIPPool
    description = forms.CharField(max_length=200, required=False)
    disabled = forms.BooleanField(required=False)
    tags = TagFilterField(model)
    tenant_group = DynamicModelChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        label=_("Tenant Group"),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_("Tenant"),
    )
    nullable_fields = ["description", "tenant"]
    fieldsets = (
        FieldSet("description", "disabled", name=_("Virtual IP Pool")),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )


class VirtualIPPoolAssignmentForm(forms.ModelForm):
    virtual_pool = DynamicModelChoiceField(
        label=_("Virtual Pool"), queryset=VirtualIPPool.objects.all()
    )
    weight = forms.IntegerField(required=True)
    disabled = forms.BooleanField(required=False)
    fieldsets = (
        FieldSet(
            ObjectAttribute("assigned_object"), "virtual_pool", "weight", "disabled"
        ),
    )

    class Meta:
        model = VirtualIPPoolAssignment
        fields = (
            "virtual_pool",
            "weight",
            "disabled",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_virtual_pool(self):
        virtual_pool = self.cleaned_data["virtual_pool"]

        conflicting_assignments = VirtualIPPoolAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            virtual_pool=virtual_pool,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return virtual_pool
