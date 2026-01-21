from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from netbox.search import SearchIndex, register_search

from netbox_load_balancing.models import Pool, HealthMonitor
from netbox_load_balancing.constants import MEMBER_ASSIGNMENT_MODELS

_all__ = ("Member", "MemberAssignment", "MemberIndex")


class Member(ContactsMixin, PrimaryModel):
    name = models.CharField(
        max_length=255,
    )
    reference = models.CharField(
        max_length=255,
    )
    ip_address = models.ForeignKey(
        to="ipam.IPAddress",
        on_delete=models.CASCADE,
        related_name="%(class)s_members",
    )
    disabled = models.BooleanField(
        default=False,
    )
    prerequisite_models = ("ipam.IPAddress",)

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Member")
        ordering = ("name", "ip_address")
        unique_together = ("ip_address", "name")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_load_balancing:member", args=[self.pk])


class MemberAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=MEMBER_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    member = models.ForeignKey(
        to="netbox_load_balancing.Member", on_delete=models.CASCADE
    )
    disabled = models.BooleanField(
        default=False,
    )
    weight = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(32767),
        ],
        default=1,
    )
    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = (
        "netbox_load_balancing.Pool",
        "netbox_load_balancing.Member",
        "netbox_load_balancing.HealthMonitor",
    )

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "member"),
                name="%(app_label)s_%(class)s_unique_member",
            ),
        )
        verbose_name = _("LB Member Assignment")
        verbose_name_plural = _("LB Member Assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.member}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class MemberIndex(SearchIndex):
    model = Member
    fields = (
        ("name", 100),
        ("reference", 200),
        ("ip_address", 300),
        ("description", 500),
    )


GenericRelation(
    to=MemberAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="pool",
).contribute_to_class(Pool, "members")

GenericRelation(
    to=MemberAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="health_monitor",
).contribute_to_class(HealthMonitor, "members")
