from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelBulkEditForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelForm,
)

from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CommentField,
    CSVModelChoiceField,
    CSVChoiceField,
)

from netbox_load_balancing.models import Listener, LBService
from netbox_load_balancing.choices import ListenerProtocolChoices

__all__ = (
    "ListenerForm",
    "ListenerFilterForm",
    "ListenerImportForm",
    "ListenerBulkEditForm",
)


class ListenerForm(PrimaryModelForm):
    name = forms.CharField(max_length=255, required=True)
    service = DynamicModelChoiceField(
        queryset=LBService.objects.all(),
        required=True,
    )
    description = forms.CharField(
        max_length=200,
        required=False,
    )
    port = forms.IntegerField(
        required=True,
        help_text=_("Listener Port"),
    )
    protocol = forms.ChoiceField(
        choices=ListenerProtocolChoices,
        required=False,
        help_text=_("Pool Protocol"),
    )
    source_nat = forms.BooleanField(
        required=False,
        help_text=_("Enable or disable SNAT"),
    )
    use_proxy_port = forms.BooleanField(
        required=False,
        help_text=_("Use Load Balancer source port when SNAT is disabled"),
    )
    max_clients = forms.IntegerField(
        required=False,
        help_text=_(
            "Maximum number of connections that can be sent on a persistent connection"
        ),
    )
    max_requests = forms.IntegerField(
        required=False,
        help_text=_(
            "Maximum number of requests that can be sent on a persistent connection"
        ),
    )
    client_timeout = forms.IntegerField(
        required=False,
        help_text=_(
            "Time in seconds after which to terminate an idle client connection"
        ),
    )
    server_timeout = forms.IntegerField(
        required=False,
        help_text=_(
            "Time in seconds after which to terminate an idle server connection"
        ),
    )
    client_keepalive = forms.BooleanField(
        required=False,
        help_text=_(
            "The Client KeepAlive mode enables the Load Balancer to process multiple requests using the same socket connection"
        ),
    )
    surge_protection = forms.BooleanField(
        required=False,
        help_text="When enabled, surge protection ensures that connections to the server occur at a rate the server can handle",
    )
    tcp_buffering = forms.BooleanField(
        required=False,
        help_text="TCP buffering option only buffers responses from the load balanced server",
    )
    compression = forms.BooleanField(
        required=False,
        help_text="Compression option allows to transparently compress HTML/TEXT files by using a set of built-in compression policies",
    )
    fieldsets = (
        FieldSet("name", "service", "description", name=_("LB Listener")),
        FieldSet(
            "port",
            "protocol",
            "source_nat",
            "use_proxy_port",
            "max_clients",
            "max_requests",
            "client_timeout",
            "server_timeout",
            "client_keepalive",
            "surge_protection",
            "tcp_buffering",
            "compression",
            name=_("Attributes"),
        ),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = Listener
        fields = [
            "name",
            "owner",
            "description",
            "service",
            "port",
            "protocol",
            "source_nat",
            "use_proxy_port",
            "max_clients",
            "max_requests",
            "client_timeout",
            "server_timeout",
            "client_keepalive",
            "surge_protection",
            "tcp_buffering",
            "compression",
            "comments",
            "tags",
        ]


class ListenerFilterForm(PrimaryModelFilterSetForm):
    model = Listener
    fieldsets = (
        FieldSet("q", "filter_id", "tag", "owner_id"),
        FieldSet("service", name=_("LB Service")),
        FieldSet(
            "port",
            "protocol",
            "source_nat",
            "use_proxy_port",
            "max_clients",
            "max_requests",
            "client_timeout",
            "server_timeout",
            "client_keepalive",
            "surge_protection",
            "tcp_buffering",
            "compression",
            name=_("Attributes"),
        ),
    )
    service = DynamicModelMultipleChoiceField(
        queryset=LBService.objects.all(),
        required=False,
    )
    port = forms.IntegerField(
        required=False,
        help_text=_("Listener Port"),
    )
    protocol = forms.ChoiceField(
        choices=ListenerProtocolChoices,
        help_text=_("Pool Protocol"),
        required=False,
    )
    source_nat = forms.BooleanField(
        required=False,
        help_text=_("Enable or disable SNAT"),
    )
    use_proxy_port = forms.BooleanField(
        required=False,
        help_text=_("Use Load Balancer source port when SNAT is disabled"),
    )
    max_clients = forms.IntegerField(
        required=False,
        help_text=_(
            "Maximum number of connections that can be sent on a persistent connection"
        ),
    )
    max_requests = forms.IntegerField(
        required=False,
        help_text=_(
            "Maximum number of requests that can be sent on a persistent connection"
        ),
    )
    client_timeout = forms.IntegerField(
        required=False,
        help_text=_(
            "Time in seconds after which to terminate an idle client connection"
        ),
    )
    server_timeout = forms.IntegerField(
        required=False,
        help_text=_(
            "Time in seconds after which to terminate an idle server connection"
        ),
    )
    client_keepalive = forms.BooleanField(
        required=False,
        help_text=_(
            "The Client KeepAlive mode enables the Load Balancer to process multiple requests using the same socket connection"
        ),
    )
    surge_protection = forms.BooleanField(
        required=False,
        help_text="When enabled, surge protection ensures that connections to the server occur at a rate the server can handle",
    )
    tcp_buffering = forms.BooleanField(
        required=False,
        help_text="TCP buffering option only buffers responses from the load balanced server",
    )
    compression = forms.BooleanField(
        required=False,
        help_text="Compression option allows to transparently compress HTML/TEXT files by using a set of built-in compression policies",
    )
    tags = TagFilterField(model)


class ListenerImportForm(PrimaryModelImportForm):
    service = CSVModelChoiceField(
        queryset=LBService.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("LB Service (address)"),
    )
    port = forms.IntegerField(
        required=True,
        help_text=_("Listener Port"),
    )
    protocol = CSVChoiceField(
        choices=ListenerProtocolChoices,
        required=False,
        help_text=_("Pool Protocol"),
    )
    source_nat = forms.BooleanField(
        required=False,
        help_text=_("Enable or disable SNAT"),
    )
    use_proxy_port = forms.BooleanField(
        required=False,
        help_text=_("Use Load Balancer source port when SNAT is disabled"),
    )
    max_clients = forms.IntegerField(
        required=False,
        help_text=_(
            "Maximum number of connections that can be sent on a persistent connection"
        ),
    )
    max_requests = forms.IntegerField(
        required=False,
        help_text=_(
            "Maximum number of requests that can be sent on a persistent connection"
        ),
    )
    client_timeout = forms.IntegerField(
        required=False,
        help_text=_(
            "Time in seconds after which to terminate an idle client connection"
        ),
    )
    server_timeout = forms.IntegerField(
        required=False,
        help_text=_(
            "Time in seconds after which to terminate an idle server connection"
        ),
    )
    client_keepalive = forms.BooleanField(
        required=False,
        help_text=_(
            "The Client KeepAlive mode enables the Load Balancer to process multiple requests using the same socket connection"
        ),
    )
    surge_protection = forms.BooleanField(
        required=False,
        help_text="When enabled, surge protection ensures that connections to the server occur at a rate the server can handle",
    )
    tcp_buffering = forms.BooleanField(
        required=False,
        help_text="TCP buffering option only buffers responses from the load balanced server",
    )
    compression = forms.BooleanField(
        required=False,
        help_text="Compression option allows to transparently compress HTML/TEXT files by using a set of built-in compression policies",
    )

    class Meta:
        model = Listener
        fields = (
            "name",
            "owner",
            "description",
            "service",
            "port",
            "protocol",
            "source_nat",
            "use_proxy_port",
            "max_clients",
            "max_requests",
            "client_timeout",
            "server_timeout",
            "client_keepalive",
            "surge_protection",
            "tcp_buffering",
            "compression",
            "tags",
        )


class ListenerBulkEditForm(PrimaryModelBulkEditForm):
    model = Listener
    description = forms.CharField(max_length=200, required=False)
    service = DynamicModelMultipleChoiceField(
        queryset=LBService.objects.all(),
        required=False,
    )
    port = forms.IntegerField(
        required=False,
        help_text=_("Listener Port"),
    )
    protocol = forms.ChoiceField(
        choices=ListenerProtocolChoices,
        help_text=_("Pool Protocol"),
        required=False,
    )
    source_nat = forms.BooleanField(
        required=False,
        help_text=_("Enable or disable SNAT"),
    )
    use_proxy_port = forms.BooleanField(
        required=False,
        help_text=_("Use Load Balancer source port when SNAT is disabled"),
    )
    max_clients = forms.IntegerField(
        required=False,
        help_text=_(
            "Maximum number of connections that can be sent on a persistent connection"
        ),
    )
    max_requests = forms.IntegerField(
        required=False,
        help_text=_(
            "Maximum number of requests that can be sent on a persistent connection"
        ),
    )
    client_timeout = forms.IntegerField(
        required=False,
        help_text=_(
            "Time in seconds after which to terminate an idle client connection"
        ),
    )
    server_timeout = forms.IntegerField(
        required=False,
        help_text=_(
            "Time in seconds after which to terminate an idle server connection"
        ),
    )
    client_keepalive = forms.BooleanField(
        required=False,
        help_text=_(
            "The Client KeepAlive mode enables the Load Balancer to process multiple requests using the same socket connection"
        ),
    )
    surge_protection = forms.BooleanField(
        required=False,
        help_text="When enabled, surge protection ensures that connections to the server occur at a rate the server can handle",
    )
    tcp_buffering = forms.BooleanField(
        required=False,
        help_text="TCP buffering option only buffers responses from the load balanced server",
    )
    compression = forms.BooleanField(
        required=False,
        help_text="Compression option allows to transparently compress HTML/TEXT files by using a set of built-in compression policies",
    )
    tags = TagFilterField(model)

    nullable_fields = ["description"]
    fieldsets = (
        FieldSet("service", "description", name=_("LB Listener")),
        FieldSet(
            "port",
            "protocol",
            "source_nat",
            "use_proxy_port",
            "max_clients",
            "max_requests",
            "client_timeout",
            "server_timeout",
            "client_keepalive",
            "surge_protection",
            "tcp_buffering",
            "compression",
            name=_("Attributes"),
        ),
        FieldSet("tags", name=_("Tags")),
    )
