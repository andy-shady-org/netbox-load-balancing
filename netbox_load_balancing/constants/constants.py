"""
Constants for filters
"""

from django.db.models import Q

SERVICE_ASSIGNMENT_MODELS = Q(
    Q(app_label="netbox_load_balancing", model="virtualip")
    | Q(app_label="dcim", model="device")
    | Q(app_label="virtualization", model="virtualmachine")
    | Q(app_label="dcim", model="virtualdevicecontext"),
)

POOL_ASSIGNMENT_MODELS = Q(
    Q(app_label="netbox_load_balancing", model="lbservice"),
)

HEALTH_MONITOR_ASSIGNMENT_MODELS = Q(
    Q(app_label="netbox_load_balancing", model="pool"),
)

MEMBER_ASSIGNMENT_MODELS = Q(
    Q(app_label="netbox_load_balancing", model="pool")
    | Q(app_label="netbox_load_balancing", model="healthmonitor"),
)

VIP_POOL_ASSIGNMENT_MODELS = Q(
    Q(app_label="ipam", model="iprange")
    | Q(app_label="ipam", model="prefix")
    | Q(app_label="ipam", model="vlan")
)
