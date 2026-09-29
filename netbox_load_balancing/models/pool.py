from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from extras.querysets import ConfigContextModelQuerySet
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from netbox.search import SearchIndex, register_search

from netbox_load_balancing.mixins import LBServiceConfigContextModelMixin
from netbox_load_balancing.models import LBService
from netbox_load_balancing.constants import POOL_ASSIGNMENT_MODELS
from netbox_load_balancing.choices import (
    PoolAlgorythmChoices,
    PoolSessionPersistenceChoices,
    PoolBackupSessionPersistenceChoices,
)

__all__ = ("Pool", "PoolAssignment", "PoolIndex")


class Pool(LBServiceConfigContextModelMixin, ContactsMixin, PrimaryModel):
    objects = ConfigContextModelQuerySet.as_manager()

    name = models.CharField(
        max_length=255,
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )
    listeners = models.ManyToManyField(
        to="netbox_load_balancing.Listener",
        related_name="%(class)s_listeners",
        blank=True,
    )
    algorythm = models.CharField(
        max_length=255,
        choices=PoolAlgorythmChoices,
        default=PoolAlgorythmChoices.LEAST_CONNECTION,
        help_text=_("Load Balancer algorythm for the pool"),
    )
    session_persistence = models.CharField(
        max_length=255,
        choices=PoolSessionPersistenceChoices,
        default=PoolSessionPersistenceChoices.SOURCE_IP,
        help_text=_("Load Balancer session persistence for the pool"),
    )
    backup_persistence = models.CharField(
        max_length=255,
        choices=PoolBackupSessionPersistenceChoices,
        default=PoolBackupSessionPersistenceChoices.NONE,
        help_text=_("Load Balancer backup session persistence for the pool"),
    )
    persistence_timeout = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1440),
        ],
        default=0,
        help_text=_("Time period for which a persistence session is in effect"),
    )
    backup_timeout = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1440),
        ],
        default=0,
        help_text=_("Time period for which a backup persistence is in effect"),
    )
    member_port = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(65535),
        ],
        blank=True,
        null=True,
        help_text=_("Backend server port if different from the listener port"),
    )
    disabled = models.BooleanField(
        default=False,
    )
    prerequisite_models = ("netbox_load_balancing.Listener",)

    class Meta:
        verbose_name = _("Pool")
        verbose_name_plural = _("Pools")
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_load_balancing:pool", args=[self.pk])

    def get_algorythm_color(self):
        return PoolAlgorythmChoices.colors.get(self.algorythm)

    def get_session_persistence_color(self):
        return PoolSessionPersistenceChoices.colors.get(self.session_persistence)

    def get_backup_persistence_color(self):
        return PoolBackupSessionPersistenceChoices.colors.get(self.backup_persistence)


class PoolAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=POOL_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    pool = models.ForeignKey(to="netbox_load_balancing.Pool", on_delete=models.CASCADE)

    clone_fields = ("assigned_object_type", "assigned_object_id")

    prerequisite_models = (
        "ipam.IPRange",
        "netbox_load_balancing.Pool",
    )

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "pool"),
                name="%(app_label)s_%(class)s_unique_pool",
            ),
        )
        verbose_name = _("LB Pool Assignment")
        verbose_name_plural = _("LB Pool Assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.pool}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class PoolIndex(SearchIndex):
    model = Pool
    fields = (
        ("name", 100),
        ("description", 500),
    )


GenericRelation(
    to=PoolAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="lbservice",
).contribute_to_class(LBService, "pools")
