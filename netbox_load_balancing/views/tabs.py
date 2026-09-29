from django.utils.translation import gettext_lazy as _
from netbox.views import generic
from utilities.views import register_model_view, ViewTab
from extras.views import ObjectConfigContextView
from netbox_load_balancing.mixins import LBServiceConfigContextViewMixin
from netbox_load_balancing.models import (
    LBService,
    HealthMonitor,
    Listener,
    Member,
    Pool,
    VirtualIP,
    VirtualIPPool,
)
from netbox_load_balancing.svg import LBServiceDiagramSVG


@register_model_view(LBService, name="diagram")
class LBServiceDiagramView(generic.ObjectView):
    queryset = LBService.objects.all()
    template_name = "netbox_load_balancing/diagram.html"
    tab = ViewTab(
        label=_("Diagram"),
        weight=500,
    )

    def get_extra_context(self, request, instance):
        base_url = request.build_absolute_uri("/")
        diagram = LBServiceDiagramSVG(instance, base_url=base_url)
        svg_drawing = diagram.render()

        hierarchy_data = diagram.data
        total_vips = len(hierarchy_data["vips"])
        total_listeners = len(hierarchy_data["listeners"])
        total_pools = len(hierarchy_data["pools"])
        total_monitors = len(hierarchy_data["health_monitors"])
        total_members = len(hierarchy_data["members"])
        total_infra = len(hierarchy_data["infra"])

        has_elements = any(
            [
                total_vips,
                total_listeners,
                total_pools,
                total_monitors,
                total_members,
                total_infra,
            ]
        )

        return {
            "svg": svg_drawing.tostring(),
            "has_elements": has_elements,
            "total_vips": total_vips,
            "total_listeners": total_listeners,
            "total_pools": total_pools,
            "total_monitors": total_monitors,
            "total_members": total_members,
            "total_infra": total_infra,
        }


class _LBServiceConfigContextBaseView(
    LBServiceConfigContextViewMixin, ObjectConfigContextView
):
    """Base view for config context tabs. Combines mixin with ObjectConfigContextView."""

    pass


@register_model_view(LBService, "configcontext", path="config-context")
class LBServiceConfigContextView(_LBServiceConfigContextBaseView):
    queryset = LBService.objects.all()
    tab = ViewTab(label=_("Config Context"), weight=2000)


@register_model_view(HealthMonitor, "configcontext", path="config-context")
class HealthMonitorConfigContextView(_LBServiceConfigContextBaseView):
    queryset = HealthMonitor.objects.all()
    tab = ViewTab(label=_("Config Context"), weight=2000)


@register_model_view(Listener, "configcontext", path="config-context")
class ListenerConfigContextView(_LBServiceConfigContextBaseView):
    queryset = Listener.objects.all()
    tab = ViewTab(label=_("Config Context"), weight=2000)


@register_model_view(VirtualIP, "configcontext", path="config-context")
class VirtualIPConfigContextView(_LBServiceConfigContextBaseView):
    queryset = VirtualIP.objects.all()
    tab = ViewTab(label=_("Config Context"), weight=2000)


@register_model_view(Member, "configcontext", path="config-context")
class MemberConfigContextView(_LBServiceConfigContextBaseView):
    queryset = Member.objects.all()
    tab = ViewTab(label=_("Config Context"), weight=2000)


@register_model_view(Pool, "configcontext", path="config-context")
class PoolConfigContextView(_LBServiceConfigContextBaseView):
    queryset = Pool.objects.all()
    tab = ViewTab(label=_("Config Context"), weight=2000)


@register_model_view(VirtualIPPool, "configcontext", path="config-context")
class VirtualIPPoolConfigContextView(_LBServiceConfigContextBaseView):
    queryset = VirtualIPPool.objects.all()
    tab = ViewTab(label=_("Config Context"), weight=2000)
