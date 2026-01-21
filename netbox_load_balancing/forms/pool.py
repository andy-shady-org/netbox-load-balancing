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
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CommentField,
    CSVModelMultipleChoiceField,
    CSVChoiceField,
)


from netbox_load_balancing.models import (
    Pool,
    PoolAssignment,
    Listener,
)
from netbox_load_balancing.choices import (
    PoolAlgorythmChoices,
    PoolSessionPersistenceChoices,
    PoolBackupSessionPersistenceChoices,
)

__all__ = (
    "PoolForm",
    "PoolFilterForm",
    "PoolImportForm",
    "PoolBulkEditForm",
    "PoolAssignmentForm",
)


class PoolForm(PrimaryModelForm):
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(max_length=200, required=False)
    disabled = forms.BooleanField(required=False)
    listeners = DynamicModelMultipleChoiceField(
        queryset=Listener.objects.all(),
        required=True,
    )
    algorythm = forms.ChoiceField(
        required=True,
        choices=PoolAlgorythmChoices,
        help_text=_("Load Balancer algorythm for the pool"),
    )
    session_persistence = forms.ChoiceField(
        required=False,
        choices=PoolSessionPersistenceChoices,
        help_text=_("Load Balancer session persistence for the pool"),
    )
    backup_persistence = forms.ChoiceField(
        required=False,
        choices=PoolBackupSessionPersistenceChoices,
        help_text=_("Load Balancer backup session persistence for the pool"),
    )
    persistence_timeout = forms.IntegerField(
        required=False,
        help_text=_("Time period for which a persistence session is in effect"),
    )
    backup_timeout = forms.IntegerField(
        required=False,
        help_text=_("Time period for which a backup persistence is in effect"),
    )
    member_port = forms.IntegerField(
        required=False,
        help_text=_("Backend server port if different from the listener port"),
    )
    fieldsets = (
        FieldSet("name", "description", "disabled", name=_("LB Pool")),
        FieldSet("listeners", name=_("LB Listeners")),
        FieldSet(
            "algorythm",
            "session_persistence",
            "backup_persistence",
            "persistence_timeout",
            "backup_timeout",
            "member_port",
            name=_("Attributes"),
        ),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = Pool
        fields = [
            "name",
            "owner",
            "description",
            "disabled",
            "listeners",
            "algorythm",
            "session_persistence",
            "backup_persistence",
            "persistence_timeout",
            "backup_timeout",
            "member_port",
            "comments",
            "tags",
        ]


class PoolFilterForm(PrimaryModelFilterSetForm):
    model = Pool
    fieldsets = (
        FieldSet("q", "filter_id", "tag", "owner_id"),
        FieldSet(
            "name",
            "listeners",
            "algorythm",
            "session_persistence",
            "backup_persistence",
            name=_("Pool"),
        ),
    )
    listeners = DynamicModelMultipleChoiceField(
        queryset=Listener.objects.all(),
        required=False,
    )
    algorythm = forms.ChoiceField(required=True, choices=PoolAlgorythmChoices)
    session_persistence = forms.ChoiceField(
        required=False, choices=PoolSessionPersistenceChoices
    )
    backup_persistence = forms.ChoiceField(
        required=False, choices=PoolBackupSessionPersistenceChoices
    )
    tags = TagFilterField(model)


class PoolImportForm(PrimaryModelImportForm):
    listeners = CSVModelMultipleChoiceField(
        queryset=Listener.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Listener (Name)"),
    )
    algorythm = CSVChoiceField(
        choices=PoolAlgorythmChoices,
        help_text=_("Load Balancer algorythm for the pool"),
        required=False,
    )
    session_persistence = CSVChoiceField(
        choices=PoolSessionPersistenceChoices,
        help_text=_("Load Balancer session persistence for the pool"),
        required=False,
    )
    backup_persistence = CSVChoiceField(
        choices=PoolBackupSessionPersistenceChoices,
        help_text=_("Load Balancer backup session persistence for the pool"),
        required=False,
    )
    persistence_timeout = forms.IntegerField(
        required=False,
        help_text=_("Time period for which a persistence session is in effect"),
    )
    backup_timeout = forms.IntegerField(
        required=False,
        help_text=_("Time period for which a backup persistence is in effect"),
    )
    member_port = forms.IntegerField(
        required=False,
        help_text=_("Backend server port if different from the listener port"),
    )
    disabled = forms.BooleanField(required=False)

    class Meta:
        model = Pool
        fields = (
            "name",
            "owner",
            "description",
            "disabled",
            "listeners",
            "algorythm",
            "session_persistence",
            "backup_persistence",
            "persistence_timeout",
            "backup_timeout",
            "member_port",
            "tags",
        )


class PoolBulkEditForm(PrimaryModelBulkEditForm):
    model = Pool
    description = forms.CharField(max_length=200, required=False)
    disabled = forms.BooleanField(required=False)
    listeners = DynamicModelMultipleChoiceField(
        queryset=Listener.objects.all(),
        required=False,
    )
    algorythm = forms.ChoiceField(
        required=False,
        choices=PoolAlgorythmChoices,
        help_text=_("Load Balancer algorythm for the pool"),
    )
    session_persistence = forms.ChoiceField(
        required=False,
        choices=PoolSessionPersistenceChoices,
        help_text=_("Load Balancer session persistence for the pool"),
    )
    backup_persistence = forms.ChoiceField(
        required=False,
        choices=PoolBackupSessionPersistenceChoices,
        help_text=_("Load Balancer backup session persistence for the pool"),
    )
    persistence_timeout = forms.IntegerField(
        required=False,
        help_text=_("Time period for which a persistence session is in effect"),
    )
    backup_timeout = forms.IntegerField(
        required=False,
        help_text=_("Time period for which a backup persistence is in effect"),
    )
    member_port = forms.IntegerField(
        required=False,
        help_text=_("Backend server port if different from the listener port"),
    )
    tags = TagFilterField(model)

    nullable_fields = ["description"]
    fieldsets = (
        FieldSet("description", "disabled", name=_("LB Pool")),
        FieldSet("listeners", name=_("LB Listeners")),
        FieldSet(
            "algorythm",
            "session_persistence",
            "backup_persistence",
            "persistence_timeout",
            "backup_timeout",
            "member_port",
            name=_("Attributes"),
        ),
        FieldSet("tags", name=_("Tags")),
    )


class PoolAssignmentForm(forms.ModelForm):
    pool = DynamicModelChoiceField(label=_("Pool"), queryset=Pool.objects.all())

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "pool"),)

    class Meta:
        model = PoolAssignment
        fields = ("pool",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_pool(self):
        pool = self.cleaned_data["pool"]

        conflicting_assignments = PoolAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            pool=pool,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return pool
