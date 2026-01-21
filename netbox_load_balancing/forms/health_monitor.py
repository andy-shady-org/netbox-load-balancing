from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelBulkEditForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelForm,
)
from utilities.forms.rendering import FieldSet, ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
    TagFilterField,
    CommentField,
    NumericArrayField,
    CSVChoiceField,
)


from netbox_load_balancing.models import (
    HealthMonitor,
    HealthMonitorAssignment,
)
from netbox_load_balancing.choices import (
    HealthMonitorTypeChoices,
    HealthMonitorHTTPVersionChoices,
)

__all__ = (
    "HealthMonitorForm",
    "HealthMonitorFilterForm",
    "HealthMonitorImportForm",
    "HealthMonitorBulkEditForm",
    "HealthMonitorAssignmentForm",
)


class HealthMonitorForm(PrimaryModelForm):
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(max_length=200, required=False)
    type = forms.ChoiceField(choices=HealthMonitorTypeChoices, required=True)
    disabled = forms.BooleanField(required=False)
    template = forms.CharField(max_length=255, required=False)
    monitor_url = forms.CharField(max_length=255, required=False)
    http_response = forms.CharField(max_length=255, required=False)
    monitor_host = forms.CharField(max_length=255, required=False)
    monitor_port = forms.IntegerField(required=False)
    http_version = forms.ChoiceField(
        choices=HealthMonitorHTTPVersionChoices,
        required=False,
        help_text=_("HTTP Version"),
    )
    http_secure = forms.BooleanField(
        required=False,
        help_text=_("Use HTTP secure connections"),
    )
    http_response_codes = NumericArrayField(
        base_field=forms.IntegerField(min_value=100, max_value=599),
        help_text="Comma-separated list of HTTP response codes considered successful for the health check. A range may be specified using a hyphen.",
        required=False,
    )
    probe_interval = forms.IntegerField(
        help_text=_("Interval in seconds between 2 probes"),
        required=False,
    )
    response_timeout = forms.IntegerField(
        required=False,
        help_text=_(
            "Amount of time in seconds for which the monitor must wait before marking the probe as failed"
        ),
    )

    fieldsets = (
        FieldSet("name", "description", "type", "disabled", name=_("LB HealthMonitor")),
        FieldSet(
            "template",
            "monitor_url",
            "http_response",
            "monitor_host",
            "monitor_port",
            "http_version",
            "http_secure",
            "http_response_codes",
            "probe_interval",
            "response_timeout",
            name=_("Attributes"),
        ),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = HealthMonitor
        fields = [
            "name",
            "owner",
            "description",
            "type",
            "disabled",
            "template",
            "monitor_url",
            "http_response",
            "monitor_host",
            "monitor_port",
            "http_version",
            "http_secure",
            "http_response_codes",
            "probe_interval",
            "response_timeout",
            "comments",
            "tags",
        ]


class HealthMonitorFilterForm(PrimaryModelFilterSetForm):
    model = HealthMonitor
    fieldsets = (
        FieldSet("q", "filter_id", "tag", "owner_id"),
        FieldSet("name", "type", "http_version", name=_("HealthMonitor")),
    )
    type = forms.ChoiceField(choices=HealthMonitorTypeChoices, required=False)
    http_version = forms.ChoiceField(
        choices=HealthMonitorHTTPVersionChoices,
        required=False,
        help_text=_("HTTP Version"),
    )
    tags = TagFilterField(model)


class HealthMonitorImportForm(PrimaryModelImportForm):
    name = forms.CharField(max_length=255, required=True)
    type = CSVChoiceField(choices=HealthMonitorTypeChoices, required=False)
    description = forms.CharField(max_length=200, required=False)
    disabled = forms.BooleanField(required=False)
    template = forms.CharField(max_length=255, required=False)
    monitor_url = forms.CharField(max_length=255, required=False)
    http_response = forms.CharField(max_length=255, required=False)
    monitor_host = forms.CharField(max_length=255, required=False)
    monitor_port = forms.IntegerField(required=False)
    http_version = CSVChoiceField(
        choices=HealthMonitorHTTPVersionChoices,
        required=False,
        help_text=_("HTTP Version"),
    )
    http_secure = forms.BooleanField(
        required=False,
        help_text=_("Use HTTP secure connections"),
    )
    http_response_codes = NumericArrayField(
        base_field=forms.IntegerField(min_value=100, max_value=599),
        help_text="Comma-separated list of HTTP response codes considered successful for the health check. A range may be specified using a hyphen.",
        required=False,
    )
    probe_interval = forms.IntegerField(
        help_text=_("Interval in seconds between 2 probes"),
        required=False,
    )
    response_timeout = forms.IntegerField(
        required=False,
        help_text=_(
            "Amount of time in seconds for which the monitor must wait before marking the probe as failed"
        ),
    )

    class Meta:
        model = HealthMonitor
        fields = (
            "name",
            "owner",
            "description",
            "type",
            "disabled",
            "template",
            "monitor_url",
            "http_response",
            "monitor_host",
            "monitor_port",
            "http_version",
            "http_secure",
            "http_response_codes",
            "probe_interval",
            "response_timeout",
            "tags",
        )


class HealthMonitorBulkEditForm(PrimaryModelBulkEditForm):
    model = HealthMonitor
    type = forms.ChoiceField(choices=HealthMonitorTypeChoices, required=False)
    description = forms.CharField(max_length=200, required=False)
    disabled = forms.BooleanField(required=False)
    template = forms.CharField(max_length=255, required=False)
    monitor_url = forms.CharField(max_length=255, required=False)
    http_response = forms.CharField(max_length=255, required=False)
    monitor_host = forms.CharField(max_length=255, required=False)
    monitor_port = forms.IntegerField(required=False)
    http_version = forms.ChoiceField(
        choices=HealthMonitorHTTPVersionChoices,
        required=False,
        help_text=_("HTTP Version"),
    )
    http_secure = forms.BooleanField(
        required=False,
        help_text=_("Use HTTP secure connections"),
    )
    http_response_codes = NumericArrayField(
        base_field=forms.IntegerField(min_value=100, max_value=599),
        help_text="Comma-separated list of HTTP response codes considered successful for the health check. A range may be specified using a hyphen.",
        required=False,
    )
    probe_interval = forms.IntegerField(
        help_text=_("Interval in seconds between 2 probes"),
        required=False,
    )
    response_timeout = forms.IntegerField(required=False)
    tags = TagFilterField(model)
    nullable_fields = ["description"]
    fieldsets = (
        FieldSet("description", "type", "disabled", name=_("LB HealthMonitor")),
        FieldSet(
            "template",
            "monitor_url",
            "http_response",
            "monitor_host",
            "monitor_port",
            "http_version",
            "http_secure",
            "http_response_codes",
            "probe_interval",
            "response_timeout",
            name=_("Attributes"),
        ),
        FieldSet("tags", name=_("Tags")),
    )


class HealthMonitorAssignmentForm(forms.ModelForm):
    monitor = DynamicModelChoiceField(
        label=_("Health Monitor"), queryset=HealthMonitor.objects.all()
    )
    weight = forms.IntegerField(required=True)
    disabled = forms.BooleanField(required=False)

    fieldsets = (
        FieldSet(ObjectAttribute("assigned_object"), "monitor", "weight", "disabled"),
    )

    class Meta:
        model = HealthMonitorAssignment
        fields = (
            "monitor",
            "weight",
            "disabled",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_monitor(self):
        monitor = self.cleaned_data["monitor"]

        conflicting_assignments = HealthMonitorAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            monitor=monitor,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return monitor
