from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from extras.querysets import ConfigContextModelQuerySet
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from netbox.search import SearchIndex, register_search
from ipam.models import IPRange, Prefix, VLAN

from netbox_load_balancing.mixins import LBServiceConfigContextModelMixin
from netbox_load_balancing.constants import VIP_POOL_ASSIGNMENT_MODELS

__all__ = ("VirtualIPPool", "VirtualIPPoolAssignment", "VirtualIPPoolIndex")


class VirtualIPPool(LBServiceConfigContextModelMixin, ContactsMixin, PrimaryModel):
    objects = ConfigContextModelQuerySet.as_manager()

    name = models.CharField()
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
        verbose_name = _("Virtual IP Pool")
        verbose_name_plural = _("Virtual IP Pools")
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_load_balancing:virtualippool", args=[self.pk])


class VirtualIPPoolAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=VIP_POOL_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    virtual_pool = models.ForeignKey(
        to="netbox_load_balancing.VirtualIPPool",
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
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
        "ipam.IPRange",
        "ipam.Prefix",
        "ipam.VLAN",
        "netbox_load_balancing.VirtualIPPool",
    )

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "virtual_pool"),
                name="%(app_label)s_%(class)s_unique_virtual_pool",
            ),
        )
        verbose_name = _("Virtual Pool Assignment")
        verbose_name_plural = _("Virtual Pool Assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.virtual_pool}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class VirtualIPPoolIndex(SearchIndex):
    model = VirtualIPPool
    fields = (
        ("name", 100),
        ("description", 500),
    )


GenericRelation(
    to=VirtualIPPoolAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="ip_range",
).contribute_to_class(IPRange, "vip_pools")

GenericRelation(
    to=VirtualIPPoolAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="prefix",
).contribute_to_class(Prefix, "vip_pools")

GenericRelation(
    to=VirtualIPPoolAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="vlan",
).contribute_to_class(VLAN, "vip_pools")
