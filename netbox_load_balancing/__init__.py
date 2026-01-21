from django.utils.translation import gettext_lazy as _
from netbox.plugins import PluginConfig
from .version import __version__


class LoadBalancingConfig(PluginConfig):
    name = "netbox_load_balancing"
    verbose_name = _("Netbox Load Balancing")
    description = _("Subsystem for tracking Load Balancing Service related objects")
    version = __version__
    author = "Andy Wilson"
    author_email = "andy@shady.org"
    base_url = "netbox-load-balancing"
    required_settings = []
    min_version = "4.5.0"
    default_settings = {
        "top_level_menu": True,
        "service_ext_page": "right",
        "pool_ext_page": "right",
        "member_ext_page": "right",
        "monitor_ext_page": "right",
    }


config = LoadBalancingConfig  # noqa
