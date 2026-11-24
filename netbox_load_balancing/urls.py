from django.urls import include, path
from utilities.urls import get_model_urls

# +
# Import views so the register_model_view is run. This is required for the
# URLs to be set up properly with get_model_urls().
# -
from .views import *  # noqa: F401

app_name = "netbox_load_balancing"

urlpatterns = [
    # Services
    path(
        "services/",
        include(get_model_urls("netbox_load_balancing", "lbservice", detail=False)),
    ),
    path(
        "services/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "lbservice")),
    ),
    # LBService Assignments
    path(
        "service-assignments/",
        include(
            get_model_urls("netbox_load_balancing", "lbserviceassignment", detail=False)
        ),
    ),
    path(
        "service-assignments/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "lbserviceassignment")),
    ),
    # Virtual Pools
    path(
        "virtual-pools/",
        include(get_model_urls("netbox_load_balancing", "virtualippool", detail=False)),
    ),
    path(
        "virtual-pools/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "virtualippool")),
    ),
    # Virtual Pool Assignments
    path(
        "virtual-pool-assignments/",
        include(
            get_model_urls(
                "netbox_load_balancing", "virtualippoolassignment", detail=False
            )
        ),
    ),
    path(
        "virtual-pool-assignments/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "virtualippoolassignment")),
    ),
    # Virtual Addresses
    path(
        "virtual-addresses/",
        include(get_model_urls("netbox_load_balancing", "virtualip", detail=False)),
    ),
    path(
        "virtual-addresses/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "virtualip")),
    ),
    # Listeners
    path(
        "listeners/",
        include(get_model_urls("netbox_load_balancing", "listener", detail=False)),
    ),
    path(
        "listeners/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "listener")),
    ),
    # Pools
    path(
        "pools/",
        include(get_model_urls("netbox_load_balancing", "pool", detail=False)),
    ),
    path(
        "pools/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "pool")),
    ),
    # Pool Assignments
    path(
        "pool-assignments/",
        include(
            get_model_urls("netbox_load_balancing", "poolassignment", detail=False)
        ),
    ),
    path(
        "pool-assignments/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "poolassignment")),
    ),
    # Health Monitors
    path(
        "health-monitors/",
        include(get_model_urls("netbox_load_balancing", "healthmonitor", detail=False)),
    ),
    path(
        "health-monitors/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "healthmonitor")),
    ),
    # Health Monitor Assignments
    path(
        "health-monitor-assignments/",
        include(
            get_model_urls(
                "netbox_load_balancing", "healthmonitorassignment", detail=False
            )
        ),
    ),
    path(
        "health-monitor-assignments/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "healthmonitorassignment")),
    ),
    # Members
    path(
        "members/",
        include(get_model_urls("netbox_load_balancing", "member", detail=False)),
    ),
    path(
        "members/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "member")),
    ),
    # Health Monitor Assignments
    path(
        "member-assignments/",
        include(
            get_model_urls("netbox_load_balancing", "memberassignment", detail=False)
        ),
    ),
    path(
        "member-assignments/<int:pk>/",
        include(get_model_urls("netbox_load_balancing", "memberassignment")),
    ),
]
