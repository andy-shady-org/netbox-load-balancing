from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from netbox.models import PrimaryModel, NetBoxModel
from netbox.models.features import ContactsMixin
from netbox.search import SearchIndex, register_search

from netbox_load_balancing.models import Pool
from netbox_load_balancing.constants import HEALTH_MONITOR_ASSIGNMENT_MODELS
from netbox_load_balancing.choices import (
    HealthMonitorTypeChoices,
    HealthMonitorHTTPVersionChoices,
)

_all__ = ("HealthMonitor", "HealthMonitorAssignment", "HealthMonitorIndex")


class HealthMonitor(ContactsMixin, PrimaryModel):
    name = models.CharField(
        max_length=255,
    )
    template = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=255,
        choices=HealthMonitorTypeChoices,
        default=HealthMonitorTypeChoices.HTTP,
    )
    monitor_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    http_response = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    monitor_host = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    monitor_port = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(65534),
        ],
        blank=True,
        null=True,
    )
    http_version = models.CharField(
        choices=HealthMonitorHTTPVersionChoices,
        default=HealthMonitorHTTPVersionChoices.VERSION_1,
        max_length=255,
        help_text=_("HTTP Version"),
    )
    http_secure = models.BooleanField(
        default=False,
        help_text=_("Use HTTP secure connections"),
    )
    http_response_codes = ArrayField(
        base_field=models.PositiveIntegerField(
            validators=[
                MinValueValidator(100),
                MaxValueValidator(599),
            ],
            default=200,
        ),
        help_text=_(
            "List of HTTP response codes considered successful for the health check"
        ),
        blank=True,
        null=True,
    )
    probe_interval = models.PositiveIntegerField(
        help_text=_("Interval in seconds between 2 probes"),
        blank=True,
        null=True,
    )
    response_timeout = models.PositiveIntegerField(
        help_text=_(
            "Amount of time in seconds for which the monitor must wait before marking the probe as failed"
        ),
        blank=True,
        null=True,
    )
    disabled = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = _("Health Monitor")
        verbose_name_plural = _("Health Monitors")
        ordering = ("name",)
        unique_together = ("name", "template")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_load_balancing:healthmonitor", args=[self.pk])

    def get_type_color(self):
        return HealthMonitorTypeChoices.colors.get(self.type)

    def get_http_version_color(self):
        return HealthMonitorHTTPVersionChoices.colors.get(self.http_version)


class HealthMonitorAssignment(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        limit_choices_to=HEALTH_MONITOR_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type", fk_field="assigned_object_id"
    )
    monitor = models.ForeignKey(
        to="netbox_load_balancing.HealthMonitor", on_delete=models.CASCADE
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
        "netbox_load_balancing.HealthMonitor",
        "netbox_load_balancing.Pool",
    )

    class Meta:
        indexes = (models.Index(fields=("assigned_object_type", "assigned_object_id")),)
        constraints = (
            models.UniqueConstraint(
                fields=("assigned_object_type", "assigned_object_id", "monitor"),
                name="%(app_label)s_%(class)s_unique_monitor",
            ),
        )
        verbose_name = _("LB Health Monitor Assignment")
        verbose_name_plural = _("LB Health Monitor Assignments")

    def __str__(self):
        return f"{self.assigned_object}: {self.monitor}"

    def get_absolute_url(self):
        if self.assigned_object:
            return self.assigned_object.get_absolute_url()
        return None


@register_search
class HealthMonitorIndex(SearchIndex):
    model = HealthMonitor
    fields = (
        ("name", 100),
        ("description", 500),
    )


GenericRelation(
    to=HealthMonitorAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="health_monitor",
).contribute_to_class(Pool, "health_monitors")
