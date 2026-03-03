from dcim.models import Device, VirtualDeviceContext
from virtualization.models import VirtualMachine
from netbox.plugins import PluginTemplateExtension
from ipam.models import Prefix, IPRange

from netbox_load_balancing.models import (
    LBServiceAssignment,
    PoolAssignment,
    HealthMonitorAssignment,
    MemberAssignment,
    HealthMonitor,
    Pool,
    VirtualIPPoolAssignment,
    VirtualIP,
)

from netbox_load_balancing.tables import (
    LBServiceAssignmentTable,
    PoolAssignmentTable,
    HealthMonitorAssignmentTable,
    MemberAssignmentTable,
    VirtualIPPoolAssignmentTable,
)


class VirtualIPContextInfo(PluginTemplateExtension):
    models = [
        "netbox_load_balancing.virtualip",
        "dcim.device",
        "dcim.virtualdevicecontext",
        "virtualization.virtualmachine",
    ]

    def right_page(self):
        """ """
        if self.context["config"].get("service_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("service_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("service_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        if isinstance(obj, Device):
            service_lists = LBServiceAssignment.objects.filter(device=obj)
        elif isinstance(obj, VirtualMachine):
            service_lists = LBServiceAssignment.objects.filter(virtualmachine=obj)
        elif isinstance(obj, VirtualDeviceContext):
            service_lists = LBServiceAssignment.objects.filter(virtualdevicecontext=obj)
        elif isinstance(obj, VirtualIP):
            service_lists = LBServiceAssignment.objects.filter(virtualip=obj)
        else:
            return ""
        service_table = LBServiceAssignmentTable(service_lists)
        return self.render(
            "netbox_load_balancing/assignments/service.html",
            extra_context={"related_service_table": service_table},
        )


class PoolContextInfo(PluginTemplateExtension):
    models = ["netbox_load_balancing.lbservice"]

    def right_page(self):
        """ """
        if self.context["config"].get("pool_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("pool_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("pool_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        pool_lists = PoolAssignment.objects.filter(lbservice=obj)
        pool_table = PoolAssignmentTable(pool_lists)
        return self.render(
            "netbox_load_balancing/assignments/pool.html",
            extra_context={"related_pool_table": pool_table},
        )


class VirtualIPPoolContextInfo(PluginTemplateExtension):
    models = ["ipam.prefix", "ipam.iprange"]

    def right_page(self):
        """ """
        if self.context["config"].get("pool_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("pool_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("pool_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        if isinstance(obj, Prefix):
            pool_lists = VirtualIPPoolAssignment.objects.filter(prefix=obj)
        elif isinstance(obj, IPRange):
            pool_lists = VirtualIPPoolAssignment.objects.filter(ip_range=obj)
        else:
            return ""
        pool_table = VirtualIPPoolAssignmentTable(pool_lists)
        return self.render(
            "netbox_load_balancing/assignments/virtualippool.html",
            extra_context={"related_pool_table": pool_table},
        )


class MemberContextInfo(PluginTemplateExtension):
    models = ["netbox_load_balancing.healthmonitor", "netbox_load_balancing.pool"]

    def right_page(self):
        """ """
        if self.context["config"].get("member_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("member_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("member_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        if isinstance(obj, HealthMonitor):
            member_lists = MemberAssignment.objects.filter(health_monitor=obj)
        elif isinstance(obj, Pool):
            member_lists = MemberAssignment.objects.filter(pool=obj)
        else:
            return ""
        member_table = MemberAssignmentTable(member_lists)
        return self.render(
            "netbox_load_balancing/assignments/member.html",
            extra_context={"related_member_table": member_table},
        )


class HealthMonitorContextInfo(PluginTemplateExtension):
    models = ["netbox_load_balancing.pool"]

    def right_page(self):
        """ """
        if self.context["config"].get("monitor_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("monitor_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("monitor_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        monitor_lists = HealthMonitorAssignment.objects.filter(health_monitor=obj)
        monitor_table = HealthMonitorAssignmentTable(monitor_lists)
        return self.render(
            "netbox_load_balancing/assignments/monitor.html",
            extra_context={"related_monitor_table": monitor_table},
        )


template_extensions = [
    VirtualIPContextInfo,
    PoolContextInfo,
    VirtualIPPoolContextInfo,
    MemberContextInfo,
    HealthMonitorContextInfo,
]
