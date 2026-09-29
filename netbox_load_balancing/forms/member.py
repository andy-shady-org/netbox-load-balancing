from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelBulkEditForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelForm,
)

from tenancy.forms import TenancyForm, TenancyFilterForm
from extras.forms import LocalConfigContextFilterForm
from utilities.forms.rendering import FieldSet, ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CommentField,
    CSVModelChoiceField,
    JSONField,
)
from ipam.models import IPAddress
from tenancy.models import Tenant, TenantGroup

from netbox_load_balancing.models import (
    Member,
    MemberAssignment,
)

__all__ = (
    "MemberForm",
    "MemberFilterForm",
    "MemberImportForm",
    "MemberBulkEditForm",
    "MemberAssignmentForm",
)


class MemberForm(TenancyForm, PrimaryModelForm):
    name = forms.CharField(max_length=255, required=True)
    ip_address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=True,
    )
    description = forms.CharField(max_length=200, required=False)
    reference = forms.CharField(max_length=255, required=False)
    disabled = forms.BooleanField(required=False)
    fieldsets = (
        FieldSet(
            "name",
            "ip_address",
            "description",
            "reference",
            "disabled",
            name=_("LB Member"),
        ),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
        FieldSet("local_context_data", name=_("Local Config Context Data")),
    )
    local_context_data = JSONField(
        required=False,
        label="",
        widget=forms.Textarea(attrs={"aria-label": _("Local config context data")}),
    )
    comments = CommentField()

    class Meta:
        model = Member
        fields = [
            "name",
            "owner",
            "description",
            "disabled",
            "ip_address",
            "reference",
            "tenant_group",
            "tenant",
            "comments",
            "tags",
            "local_context_data",
        ]


class MemberFilterForm(LocalConfigContextFilterForm, PrimaryModelFilterSetForm):
    model = Member
    fieldsets = (
        FieldSet("q", "filter_id", "tag", "owner_id"),
        FieldSet("name", "ip_address", "reference", "disabled", name=_("LB Member")),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
        FieldSet("local_context_data", name=_("Local Config Context Data")),
    )
    ip_address = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
    )
    name = forms.CharField(max_length=255, required=False)
    reference = forms.CharField(max_length=255, required=False)
    disabled = forms.BooleanField(required=False)
    tags = TagFilterField(model)


class MemberImportForm(PrimaryModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Tenant"),
    )
    name = forms.CharField(max_length=255, required=True)
    ip_address = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=True,
        to_field_name="address",
        help_text=_("IP Address (address)"),
    )
    disabled = forms.BooleanField(required=False)

    class Meta:
        model = Member
        fields = (
            "name",
            "owner",
            "ip_address",
            "reference",
            "description",
            "disabled",
            "tags",
            "local_context_data",
        )


class MemberBulkEditForm(PrimaryModelBulkEditForm):
    model = Member
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
    description = forms.CharField(max_length=200, required=False)
    disabled = forms.BooleanField(required=False)
    ip_address = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
    )
    tags = TagFilterField(model)

    nullable_fields = ["description"]
    fieldsets = (
        FieldSet(
            "ip_address", "description", "reference", "disabled", name=_("LB Member")
        ),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )


class MemberAssignmentForm(forms.ModelForm):
    member = DynamicModelChoiceField(label=_("Member"), queryset=Member.objects.all())
    weight = forms.IntegerField(required=True)
    disabled = forms.BooleanField(required=False)

    fieldsets = (
        FieldSet(ObjectAttribute("assigned_object"), "member", "weight", "disabled"),
    )

    class Meta:
        model = MemberAssignment
        fields = (
            "member",
            "weight",
            "disabled",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_member(self):
        member = self.cleaned_data["member"]

        conflicting_assignments = MemberAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            member=member,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return member
