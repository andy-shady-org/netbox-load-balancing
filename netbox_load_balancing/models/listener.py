from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from netbox.models import PrimaryModel
from netbox.models.features import ContactsMixin
from netbox.search import SearchIndex, register_search

from netbox_load_balancing.choices import ListenerProtocolChoices

_all__ = ("Listener", "ListenerIndex")


class Listener(ContactsMixin, PrimaryModel):
    name = models.CharField(
        max_length=255,
    )
    service = models.ForeignKey(
        to="netbox_load_balancing.LBService",
        on_delete=models.CASCADE,
        related_name="%(class)s_service",
    )
    port = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(65534),
        ],
        help_text=_("Listener Port"),
    )
    protocol = models.CharField(
        max_length=255,
        choices=ListenerProtocolChoices,
        default=ListenerProtocolChoices.TCP,
        help_text=_("Pool Protocol"),
    )
    source_nat = models.BooleanField(
        default=True, help_text=_("Enable or disable SNAT")
    )
    use_proxy_port = models.BooleanField(
        default=False,
        help_text=_("Use Load Balancer source port when SNAT is disabled"),
    )
    max_clients = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4294967295),
        ],
        default=0,
        help_text=_(
            "Maximum number of connections that can be sent on a persistent connection"
        ),
    )
    max_requests = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4294967295),
        ],
        default=0,
        help_text=_(
            "Maximum number of requests that can be sent on a persistent connection"
        ),
    )
    client_timeout = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(31536000),
        ],
        default=9000,
        help_text=_(
            "Time in seconds after which to terminate an idle client connection"
        ),
    )
    server_timeout = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(31536000),
        ],
        default=9000,
        help_text=_(
            "Time in seconds after which to terminate an idle server connection"
        ),
    )
    client_keepalive = models.BooleanField(
        default=False,
        help_text=_(
            "The Client KeepAlive mode enables the Load Balancer to process multiple requests using the same socket connection"
        ),
    )
    surge_protection = models.BooleanField(
        default=False,
        help_text="When enabled, surge protection ensures that connections to the server occur at a rate the server can handle",
    )
    tcp_buffering = models.BooleanField(
        default=False,
        help_text="TCP buffering option only buffers responses from the load balanced server",
    )
    compression = models.BooleanField(
        default=False,
        help_text="Compression option allows to transparently compress HTML/TEXT files by using a set of built-in compression policies",
    )
    prerequisite_models = ("netbox_load_balancing.LBService",)

    class Meta:
        verbose_name = _("Listener")
        verbose_name_plural = _("Listeners")
        ordering = ("name", "port")
        unique_together = ("name", "service")

    def __str__(self):
        return f"{self.name}: {self.port}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_load_balancing:listener", args=[self.pk])

    def get_protocol_color(self):
        return ListenerProtocolChoices.colors.get(self.protocol)


@register_search
class ListenerIndex(SearchIndex):
    model = Listener
    fields = (
        ("name", 100),
        ("description", 500),
    )
