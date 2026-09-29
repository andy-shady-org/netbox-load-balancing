from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from extras.querysets import ConfigContextModelQuerySet
from netbox.models import PrimaryModel
from netbox.models.features import ContactsMixin
from netbox.search import SearchIndex, register_search
from ipam.validators import DNSValidator

from netbox_load_balancing.mixins import LBServiceConfigContextModelMixin

__all__ = ("VirtualIP", "VirtualIPIndex")


class VirtualIP(ContactsMixin, LBServiceConfigContextModelMixin, PrimaryModel):
    objects = ConfigContextModelQuerySet.as_manager()

    name = models.CharField(max_length=255)
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )
    dns_name = models.CharField(
        max_length=255,
        blank=True,
        validators=[DNSValidator],
        verbose_name=_("DNS name"),
        help_text=_("Hostname or FQDN (not case-sensitive)"),
    )
    disabled = models.BooleanField(
        default=False,
    )
    virtual_pool = models.ForeignKey(
        to="netbox_load_balancing.VirtualIPPool",
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
    )
    address = models.ForeignKey(
        to="ipam.IPAddress",
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
    )
    route_health_injection = models.BooleanField(
        default=False,
        help_text=_("Enable Route Health Injection on this Virtual IP"),
    )

    class Meta:
        verbose_name = _("Virtual IP")
        verbose_name_plural = _("Virtual IPs")
        ordering = ("name", "virtual_pool")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_load_balancing:virtualip", args=[self.pk])


@register_search
class VirtualIPIndex(SearchIndex):
    model = VirtualIP
    fields = (
        ("name", 100),
        ("dns_name", 100),
        ("description", 500),
    )
