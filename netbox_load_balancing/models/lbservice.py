from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from dcim.models import Device, VirtualDeviceContext
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from netbox.search import SearchIndex, register_search

from netbox_load_balancing.constants import SERVICE_ASSIGNMENT_MODELS
from netbox_load_balancing.models import VirtualIP

_all__ = ("LBService", "LBServiceAssignment", "ServiceIndex")


class LBService(ContactsMixin, PrimaryModel):
    name = models.CharField(
        max_length=255,
    )
    reference = models.CharField(
        max_length=255,
    )
    disabled = models.BooleanField(
        default=False,
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("LB Service")
        verbose_name_plural = _("LB Services")
        ordering = ("name", "reference")
        unique_together = ("name", "reference")

    def __str__(self):
        return f"{self.name}: {self.reference}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_load_balancing:lbservice", args=[self.pk])


class LBServiceAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=SERVICE_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    service = models.ForeignKey(
        to="netbox_load_balancing.LBService", on_delete=models.CASCADE
    )

    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = (
        "dcim.Device",
        "dcim.VirtualDeviceContext",
        "netbox_load_balancing.VirtualIP",
        "netbox_load_balancing.LBService",
    )

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "service"),
                name="%(app_label)s_%(class)s_unique_service",
            ),
        )
        verbose_name = _("LB Service Assignment")
        verbose_name_plural = _("LB Service Assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.service}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class LBServiceIndex(SearchIndex):
    model = LBService
    fields = (
        ("name", 100),
        ("reference", 300),
        ("description", 500),
    )


GenericRelation(
    to=LBServiceAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualip",
).contribute_to_class(VirtualIP, "lbservices")

GenericRelation(
    to=LBServiceAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="device",
).contribute_to_class(Device, "lbservices")

GenericRelation(
    to=LBServiceAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="virtualdevicecontext",
).contribute_to_class(VirtualDeviceContext, "lbservices")
