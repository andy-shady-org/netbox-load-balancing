import svgwrite
from svgwrite.container import Group, Hyperlink
from svgwrite.path import Path
from svgwrite.shapes import Circle, Rect
from svgwrite.text import Text

from django.contrib.contenttypes.models import ContentType
from django.db import models

from dcim.models import Device, VirtualDeviceContext
from virtualization.models import VirtualMachine

from netbox_load_balancing.models import (
    HealthMonitor,
    HealthMonitorAssignment,
    LBService,
    Listener,
    MemberAssignment,
    Pool,
    PoolAssignment,
    VirtualIP,
    VirtualIPPoolAssignment,
)

__all__ = (
    "LBServiceDiagramSVG",
    "get_lbservice_hierarchy_data",
)


def get_lbservice_hierarchy_data(instance):
    """
    Extract and structure the complete Northbound and Southbound relationships
    for a given LBService instance.
    """
    data = {
        "service": {
            "id": instance.pk,
            "name": instance.name,
            "reference": instance.reference,
            "disabled": instance.disabled,
            "tenant": str(instance.tenant) if instance.tenant else None,
            "url": instance.get_absolute_url(),
        },
        "infra": [],
        "vip_pools": {},
        "vips": [],
        "listeners": [],
        "pools": [],
        "health_monitors": [],
        "members": [],
        "edges": [],  # List of dicts: {'source': id, 'target': id, 'style': 'solid'|'dashed', 'label': ''}
    }

    # 1. Northbound Host Infrastructure Assignments
    # Device
    for device in Device.objects.filter(lbservices__service=instance).distinct():
        infra_id = f"device_{device.pk}"
        data["infra"].append(
            {
                "id": infra_id,
                "type": "Device",
                "name": str(device),
                "url": device.get_absolute_url(),
                "disabled": False,
            }
        )
        data["edges"].append(
            {
                "source": infra_id,
                "target": f"service_{instance.pk}",
                "style": "solid",
                "label": "Host",
            }
        )

    # Virtual Machine
    for vm in VirtualMachine.objects.filter(lbservices__service=instance).distinct():
        infra_id = f"vm_{vm.pk}"
        data["infra"].append(
            {
                "id": infra_id,
                "type": "Virtual Machine",
                "name": str(vm),
                "url": vm.get_absolute_url(),
                "disabled": False,
            }
        )
        data["edges"].append(
            {
                "source": infra_id,
                "target": f"service_{instance.pk}",
                "style": "solid",
                "label": "Host",
            }
        )

    # Virtual Device Context
    for vdc in VirtualDeviceContext.objects.filter(
        lbservices__service=instance
    ).distinct():
        infra_id = f"vdc_{vdc.pk}"
        data["infra"].append(
            {
                "id": infra_id,
                "type": "VDC",
                "name": str(vdc),
                "url": vdc.get_absolute_url(),
                "disabled": False,
            }
        )
        data["edges"].append(
            {
                "source": infra_id,
                "target": f"service_{instance.pk}",
                "style": "solid",
                "label": "Host",
            }
        )

    # 2. Northbound Virtual IPs and VIP Pools
    vips = (
        VirtualIP.objects.filter(lbservices__service=instance)
        .select_related("virtual_pool", "address")
        .distinct()
    )
    seen_vip_pools = set()

    for vip in vips:
        vip_node_id = f"vip_{vip.pk}"
        vip_data = {
            "id": vip_node_id,
            "name": vip.name,
            "address": str(vip.address) if vip.address else "",
            "dns_name": vip.dns_name,
            "disabled": vip.disabled,
            "url": vip.get_absolute_url(),
            "pool_id": None,
        }

        # Parent VirtualIPPool
        if vip.virtual_pool:
            pool = vip.virtual_pool
            pool_node_id = f"vippool_{pool.pk}"
            vip_data["pool_id"] = pool_node_id

            if pool.pk not in seen_vip_pools:
                seen_vip_pools.add(pool.pk)
                # Query underlying assignments (IPRange, Prefix, VLAN)
                subnets = []
                for assignment in VirtualIPPoolAssignment.objects.filter(
                    virtual_pool=pool
                ).select_related("assigned_object_type"):
                    assigned_obj = assignment.assigned_object
                    if assigned_obj:
                        type_name = assigned_obj._meta.verbose_name
                        subnets.append(
                            {
                                "type": type_name,
                                "name": str(assigned_obj),
                                "url": (
                                    assigned_obj.get_absolute_url()
                                    if hasattr(assigned_obj, "get_absolute_url")
                                    else None
                                ),
                            }
                        )

                data["vip_pools"][pool_node_id] = {
                    "id": pool_node_id,
                    "name": pool.name,
                    "disabled": pool.disabled,
                    "url": pool.get_absolute_url(),
                    "subnets": subnets,
                }

            # Edge from VIP Pool to VIP
            data["edges"].append(
                {
                    "source": pool_node_id,
                    "target": vip_node_id,
                    "style": "solid",
                    "label": "",
                }
            )

        data["vips"].append(vip_data)

        # Edge from VIP to LBService
        data["edges"].append(
            {
                "source": vip_node_id,
                "target": f"service_{instance.pk}",
                "style": "solid",
                "label": "VIP",
            }
        )

    # 3. Southbound Listeners
    listeners = Listener.objects.filter(service=instance)
    for listener in listeners:
        listener_node_id = f"listener_{listener.pk}"
        data["listeners"].append(
            {
                "id": listener_node_id,
                "name": listener.name,
                "protocol": listener.protocol,
                "port": listener.port,
                "url": listener.get_absolute_url(),
            }
        )

        # Edge from LBService to Listener
        data["edges"].append(
            {
                "source": f"service_{instance.pk}",
                "target": listener_node_id,
                "style": "solid",
                "label": (
                    f"{listener.protocol.upper()}:{listener.port}"
                    if listener.port
                    else listener.protocol.upper()
                ),
            }
        )

    # 4. Southbound Pools
    # Pools can be linked directly via ManyToManyField `listeners` or via PoolAssignment to LBService
    lbservice_type = ContentType.objects.get_for_model(LBService)
    pool_assignments = PoolAssignment.objects.filter(
        assigned_object_type=lbservice_type,
        assigned_object_id=instance.pk,
    ).values_list("pool_id", flat=True)

    pools = Pool.objects.filter(
        models.Q(listeners__in=listeners) | models.Q(pk__in=pool_assignments)
    ).distinct()

    pool_content_type = ContentType.objects.get_for_model(Pool)
    health_monitor_content_type = ContentType.objects.get_for_model(HealthMonitor)

    seen_monitors = set()
    seen_members = {}

    for pool in pools:
        pool_node_id = f"pool_{pool.pk}"
        pool_listeners = pool.listeners.filter(service=instance)

        data["pools"].append(
            {
                "id": pool_node_id,
                "name": pool.name,
                "algorythm": (
                    pool.get_algorythm_display()
                    if hasattr(pool, "get_algorythm_display")
                    else pool.algorythm
                ),
                "session_persistence": (
                    pool.get_session_persistence_display()
                    if hasattr(pool, "get_session_persistence_display")
                    else pool.session_persistence
                ),
                "disabled": pool.disabled,
                "url": pool.get_absolute_url(),
            }
        )

        # Connect listeners to this pool
        for listener in pool_listeners:
            data["edges"].append(
                {
                    "source": f"listener_{listener.pk}",
                    "target": pool_node_id,
                    "style": "solid",
                    "label": "",
                }
            )

        # If pool was assigned to LBService without listener
        if not pool_listeners and pool.pk in pool_assignments:
            data["edges"].append(
                {
                    "source": f"service_{instance.pk}",
                    "target": pool_node_id,
                    "style": "solid",
                    "label": "Direct Pool",
                }
            )

        # Health Monitors attached to this pool
        monitor_assignments = HealthMonitorAssignment.objects.filter(
            assigned_object_type=pool_content_type,
            assigned_object_id=pool.pk,
        ).select_related("monitor")

        for hm_assignment in monitor_assignments:
            monitor = hm_assignment.monitor
            monitor_node_id = f"hm_{monitor.pk}"

            if monitor.pk not in seen_monitors:
                seen_monitors.add(monitor.pk)
                data["health_monitors"].append(
                    {
                        "id": monitor_node_id,
                        "name": monitor.name,
                        "type": (
                            monitor.get_type_display()
                            if hasattr(monitor, "get_type_display")
                            else monitor.type
                        ),
                        "monitor_url": monitor.monitor_url,
                        "monitor_port": monitor.monitor_port,
                        "http_version": (
                            monitor.get_http_version_display()
                            if hasattr(monitor, "get_http_version_display")
                            else monitor.http_version
                        ),
                        "disabled": monitor.disabled or hm_assignment.disabled,
                        "url": monitor.get_absolute_url(),
                    }
                )

            # Health monitor monitors the pool (dashed line)
            data["edges"].append(
                {
                    "source": monitor_node_id,
                    "target": pool_node_id,
                    "style": "dashed",
                    "label": "Monitors",
                }
            )

            # Health monitor also monitors listeners associated with the pool
            for listener in pool_listeners:
                data["edges"].append(
                    {
                        "source": monitor_node_id,
                        "target": f"listener_{listener.pk}",
                        "style": "dashed",
                        "label": "Monitors",
                    }
                )

        # Members attached to this pool
        member_assignments = MemberAssignment.objects.filter(
            assigned_object_type=pool_content_type,
            assigned_object_id=pool.pk,
        ).select_related("member", "member__ip_address")

        for m_assignment in member_assignments:
            member = m_assignment.member
            member_node_id = f"member_{member.pk}"

            if member.pk not in seen_members:
                seen_members[member.pk] = {
                    "id": member_node_id,
                    "name": member.name,
                    "ip_address": str(member.ip_address) if member.ip_address else "",
                    "reference": member.reference,
                    "disabled": member.disabled or m_assignment.disabled,
                    "url": member.get_absolute_url(),
                }

            # Edge from Pool to Member
            data["edges"].append(
                {
                    "source": pool_node_id,
                    "target": member_node_id,
                    "style": "solid",
                    "label": (
                        f"w:{m_assignment.weight}" if m_assignment.weight > 1 else ""
                    ),
                }
            )

    # Also check members attached to health monitors directly
    for monitor_dict in data["health_monitors"]:
        m_pk = int(monitor_dict["id"].replace("hm_", ""))
        hm_member_assignments = MemberAssignment.objects.filter(
            assigned_object_type=health_monitor_content_type,
            assigned_object_id=m_pk,
        ).select_related("member", "member__ip_address")

        for m_assignment in hm_member_assignments:
            member = m_assignment.member
            member_node_id = f"member_{member.pk}"
            if member.pk not in seen_members:
                seen_members[member.pk] = {
                    "id": member_node_id,
                    "name": member.name,
                    "ip_address": str(member.ip_address) if member.ip_address else "",
                    "reference": member.reference,
                    "disabled": member.disabled or m_assignment.disabled,
                    "url": member.get_absolute_url(),
                }
            data["edges"].append(
                {
                    "source": monitor_dict["id"],
                    "target": member_node_id,
                    "style": "dashed",
                    "label": "Probes",
                }
            )

    data["members"] = list(seen_members.values())
    return data


class LBServiceDiagramSVG:
    """
    Renders an interactive SVG diagram representing the complete load balancing service hierarchy.
    """

    NODE_WIDTH = 220
    NODE_HEIGHT = 70
    X_GAP = 40
    Y_GAP = 60
    PADDING = 40

    # Color palette
    COLORS = {
        "infra": {
            "bg": "581c87",
            "header": "3b0764",
            "border": "7e22ce",
            "accent": "c084fc",
        },
        "vippool": {
            "bg": "0f766e",
            "header": "115e59",
            "border": "14b8a6",
            "accent": "2dd4bf",
        },
        "vip": {
            "bg": "0369a1",
            "header": "075985",
            "border": "0284c7",
            "accent": "38bdf8",
        },
        "service": {
            "bg": "1d4ed8",
            "header": "1e40af",
            "border": "3b82f6",
            "accent": "60a5fa",
        },
        "listener": {
            "bg": "15803d",
            "header": "166534",
            "border": "22c55e",
            "accent": "4ade80",
        },
        "pool": {
            "bg": "c2410c",
            "header": "9a3412",
            "border": "ea580c",
            "accent": "fb923c",
        },
        "monitor": {
            "bg": "be123c",
            "header": "9f1239",
            "border": "e11d48",
            "accent": "fb7185",
        },
        "member": {
            "bg": "334155",
            "header": "1e293b",
            "border": "475569",
            "accent": "94a3b8",
        },
    }

    def __init__(self, service, base_url=""):
        self.service = service
        self.base_url = base_url.rstrip("/")
        self.data = get_lbservice_hierarchy_data(service)
        self.node_positions = (
            {}
        )  # node_id -> (cx, cy, top_pt, bottom_pt, left_pt, right_pt)
        self.node_boxes = {}  # node_id -> (x, y, w, h)

    def _qualify_url(self, url):
        if not url:
            return "#"
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return f"{self.base_url}{url}"

    def build_layout(self):
        """
        Organize nodes into vertical tiers and compute coordinates.
        Tiers:
          0: Northbound Infra & VIP Pools
          1: Northbound VIPs
          2: Core LBService
          3: Southbound Listeners
          4: Southbound Pools & Health Monitors
          5: Southbound Members
        """
        tiers = [
            [],  # Tier 0: Infra + VIP Pools
            [],  # Tier 1: VIPs
            [],  # Tier 2: LBService
            [],  # Tier 3: Listeners
            [],  # Tier 4: Pools + Health Monitors
            [],  # Tier 5: Members
        ]

        # Tier 0: Infra items on left, VIP Pools on right
        for item in self.data["infra"]:
            tiers[0].append((item["id"], "infra", item))
        for pool_id, pool_data in self.data["vip_pools"].items():
            tiers[0].append((pool_id, "vippool", pool_data))

        # Tier 1: VIPs
        for vip in self.data["vips"]:
            tiers[1].append((vip["id"], "vip", vip))

        # Tier 2: Core Service
        service_id = f"service_{self.service.pk}"
        tiers[2].append((service_id, "service", self.data["service"]))

        # Tier 3: Listeners
        for listener in self.data["listeners"]:
            tiers[3].append((listener["id"], "listener", listener))

        # Tier 4: Pools & Health Monitors (alternate or interleave)
        for pool in self.data["pools"]:
            tiers[4].append((pool["id"], "pool", pool))
        for hm in self.data["health_monitors"]:
            tiers[4].append((hm["id"], "monitor", hm))

        # Tier 5: Members
        for member in self.data["members"]:
            tiers[5].append((member["id"], "member", member))

        # Calculate max items per tier to determine total SVG width
        max_items_in_tier = max(len(tier) for tier in tiers) if any(tiers) else 1
        max_items_in_tier = max(max_items_in_tier, 1)

        total_content_width = (
            max_items_in_tier * self.NODE_WIDTH + (max_items_in_tier - 1) * self.X_GAP
        )
        svg_width = max(total_content_width + self.PADDING * 2, 900)

        # Filter out empty tiers to prevent unnecessary vertical gaps, but keep order
        active_tiers = [(i, tier) for i, tier in enumerate(tiers) if tier]

        current_y = self.PADDING
        for tier_idx, tier_items in active_tiers:
            count = len(tier_items)
            tier_width = count * self.NODE_WIDTH + (count - 1) * self.X_GAP
            start_x = (svg_width - tier_width) / 2

            for item_idx, (node_id, node_type, item_data) in enumerate(tier_items):
                node_x = start_x + item_idx * (self.NODE_WIDTH + self.X_GAP)
                node_y = current_y

                # Adjust height if node has subnets or extra attributes
                extra_height = 0
                if node_type == "vippool" and item_data.get("subnets"):
                    extra_height = min(len(item_data["subnets"]), 2) * 16
                node_h = self.NODE_HEIGHT + extra_height

                cx = node_x + self.NODE_WIDTH / 2
                cy = node_y + node_h / 2
                top_pt = (cx, node_y)
                bottom_pt = (cx, node_y + node_h)
                left_pt = (node_x, cy)
                right_pt = (node_x + self.NODE_WIDTH, cy)

                self.node_boxes[node_id] = (
                    node_x,
                    node_y,
                    self.NODE_WIDTH,
                    node_h,
                    node_type,
                    item_data,
                )
                self.node_positions[node_id] = {
                    "cx": cx,
                    "cy": cy,
                    "top": top_pt,
                    "bottom": bottom_pt,
                    "left": left_pt,
                    "right": right_pt,
                    "tier": tier_idx,
                }

            # Increment Y for next tier
            max_h = max(
                (self.node_boxes[nid][3] for nid, _, _ in tier_items),
                default=self.NODE_HEIGHT,
            )
            current_y += max_h + self.Y_GAP

        svg_height = current_y - self.Y_GAP + self.PADDING
        return svg_width, svg_height

    def render(self):
        """
        Produce and return the svgwrite Drawing object.
        """
        svg_width, svg_height = self.build_layout()

        drawing = svgwrite.Drawing(
            size=(f"{svg_width}px", f"{svg_height}px"),
            viewBox=f"0 0 {svg_width} {svg_height}",
        )

        # SVG Defs & CSS Styling
        defs = drawing.defs
        style = drawing.style("""
            .diagram-bg { fill: #f8fafc; }
            .node-link { text-decoration: none; cursor: pointer; }
            .node-box { transition: filter 0.15s ease-in-out, transform 0.15s ease-in-out; }
            .node-link:hover .node-box { filter: brightness(1.15) drop-shadow(0 4px 6px rgba(0,0,0,0.3)); }
            .node-title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 13px; font-weight: 600; }
            .node-type { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
            .node-detail { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 11px; }
            .edge-line { stroke: #64748b; stroke-width: 2px; fill: none; }
            .edge-dashed { stroke: #e11d48; stroke-width: 1.8px; stroke-dasharray: 5,4; fill: none; opacity: 0.85; }
            .edge-label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; fill: #475569; font-weight: 500; text-anchor: middle; }
            .edge-label-bg { fill: #ffffff; opacity: 0.9; rx: 3px; }
            .badge-disabled { fill: #ef4444; font-size: 9px; font-weight: bold; }
            """)
        defs.add(style)

        # Draw Background
        drawing.add(Rect((0, 0), (svg_width, svg_height), class_="diagram-bg", rx=12))

        # 1. Draw Connectors / Edges first so nodes sit on top
        edges_group = Group(id="diagram-edges")
        drawn_edges = set()

        for edge in self.data["edges"]:
            src_id = edge["source"]
            tgt_id = edge["target"]
            style_type = edge.get("style", "solid")
            label = edge.get("label", "")

            edge_key = (src_id, tgt_id, style_type)
            if edge_key in drawn_edges:
                continue
            drawn_edges.add(edge_key)

            if src_id not in self.node_positions or tgt_id not in self.node_positions:
                continue

            src_pos = self.node_positions[src_id]
            tgt_pos = self.node_positions[tgt_id]

            # Determine connection points based on relative tier
            if src_pos["tier"] < tgt_pos["tier"]:
                start_pt = src_pos["bottom"]
                end_pt = tgt_pos["top"]
            elif src_pos["tier"] > tgt_pos["tier"]:
                start_pt = src_pos["top"]
                end_pt = tgt_pos["bottom"]
            else:
                # Same tier
                if src_pos["cx"] < tgt_pos["cx"]:
                    start_pt = src_pos["right"]
                    end_pt = tgt_pos["left"]
                else:
                    start_pt = src_pos["left"]
                    end_pt = tgt_pos["right"]

            # Draw smooth cubic bezier curve
            x1, y1 = start_pt
            x2, y2 = end_pt
            mid_y = (y1 + y2) / 2
            path_d = f"M {x1} {y1} C {x1} {mid_y}, {x2} {mid_y}, {x2} {y2}"

            css_class = "edge-dashed" if style_type == "dashed" else "edge-line"
            edges_group.add(Path(d=path_d, class_=css_class))

            # Edge Label if present
            if label:
                lx = (x1 + x2) / 2
                ly = mid_y
                label_w = len(label) * 6 + 10
                label_h = 14
                edges_group.add(
                    Rect(
                        (lx - label_w / 2, ly - label_h / 2 - 2),
                        (label_w, label_h),
                        class_="edge-label-bg",
                    )
                )
                edges_group.add(Text(label, insert=(lx, ly + 2), class_="edge-label"))

        drawing.add(edges_group)

        # 2. Draw Nodes
        nodes_group = Group(id="diagram-nodes")

        for node_id, (nx, ny, nw, nh, ntype, ndata) in self.node_boxes.items():
            color_cfg = self.COLORS.get(ntype, self.COLORS["service"])
            url = self._qualify_url(ndata.get("url"))

            link = Hyperlink(href=url, target="_parent", class_="node-link")

            # Main Node Container Rect
            node_rect = Rect(
                (nx, ny),
                (nw, nh),
                rx=8,
                ry=8,
                fill=f"#{color_cfg['bg']}",
                stroke=f"#{color_cfg['border']}",
                stroke_width=1.5,
                class_="node-box",
            )
            link.add(node_rect)

            # Header / Type Bar
            header_h = 22
            header_rect = Rect(
                (nx, ny),
                (nw, header_h),
                rx=8,
                ry=8,
                fill=f"#{color_cfg['header']}",
            )
            link.add(header_rect)
            # Square bottom corners of header
            link.add(
                Rect((nx, ny + header_h - 4), (nw, 4), fill=f"#{color_cfg['header']}")
            )

            # Header Type Label
            type_text = ntype.upper()
            if ntype == "infra":
                type_text = ndata.get("type", "INFRASTRUCTURE").upper()
            elif ntype == "vippool":
                type_text = "VIP POOL"
            elif ntype == "vip":
                type_text = "VIRTUAL IP"
            elif ntype == "service":
                type_text = "LB SERVICE"
            elif ntype == "monitor":
                type_text = f"MONITOR ({ndata.get('type', 'HM')})"

            link.add(
                Text(
                    type_text,
                    insert=(nx + 10, ny + 15),
                    fill=f"#{color_cfg['accent']}",
                    class_="node-type",
                )
            )

            # Disabled Badge / Indicator if disabled
            if ndata.get("disabled"):
                link.add(Circle(center=(nx + nw - 14, ny + 11), r=4, fill="#ef4444"))
                link.add(
                    Text(
                        "OFF",
                        insert=(nx + nw - 38, ny + 15),
                        fill="#ef4444",
                        class_="node-type",
                    )
                )
            else:
                link.add(Circle(center=(nx + nw - 14, ny + 11), r=4, fill="#22c55e"))

            # Node Name / Title
            name_text = str(ndata.get("name", ""))
            if len(name_text) > 26:
                name_text = name_text[:24] + "…"
            link.add(
                Text(
                    name_text,
                    insert=(nx + 10, ny + 39),
                    fill="#ffffff",
                    class_="node-title",
                )
            )

            # Details Line
            detail_line = ""
            if ntype == "service":
                ref = ndata.get("reference")
                tenant = ndata.get("tenant")
                parts = []
                if ref:
                    parts.append(f"Ref: {ref}")
                if tenant:
                    parts.append(f"Tenant: {tenant}")
                detail_line = " | ".join(parts)
            elif ntype == "vip":
                addr = ndata.get("address")
                dns = ndata.get("dns_name")
                detail_line = f"IP: {addr}" if addr else ""
                if dns:
                    detail_line += f" ({dns})"
            elif ntype == "vippool":
                subnets = ndata.get("subnets", [])
                if subnets:
                    detail_line = ", ".join(
                        f"{s['type']}: {s['name']}" for s in subnets[:2]
                    )
                else:
                    detail_line = "No assigned subnets"
            elif ntype == "listener":
                proto = ndata.get("protocol", "TCP").upper()
                port = ndata.get("port")
                detail_line = (
                    f"Protocol: {proto}:{port}" if port else f"Protocol: {proto}"
                )
            elif ntype == "pool":
                algo = ndata.get("algorythm", "")
                sess = ndata.get("session_persistence", "")
                detail_line = f"Algo: {algo}"
                if sess:
                    detail_line += f" | {sess}"
            elif ntype == "monitor":
                m_url = ndata.get("monitor_url")
                m_port = ndata.get("monitor_port")
                if m_url:
                    detail_line = f"URL: {m_url}"
                elif m_port:
                    detail_line = f"Port: {m_port}"
                else:
                    detail_line = f"Version: {ndata.get('http_version', '1.1')}"
            elif ntype == "member":
                ip = ndata.get("ip_address", "")
                ref = ndata.get("reference", "")
                detail_line = f"IP: {ip}" if ip else ""
                if ref:
                    detail_line += f" [{ref}]"
            elif ntype == "infra":
                detail_line = ndata.get("type", "Host")

            if len(detail_line) > 30:
                detail_line = detail_line[:28] + "…"

            if detail_line:
                link.add(
                    Text(
                        detail_line,
                        insert=(nx + 10, ny + 56),
                        fill=f"#{color_cfg['accent']}",
                        class_="node-detail",
                    )
                )

            # If VIP Pool has additional subnet lines
            if (
                ntype == "vippool"
                and ndata.get("subnets")
                and len(ndata["subnets"]) > 1
            ):
                cursor_y = ny + 72
                for s in ndata["subnets"][1:2]:
                    sub_text = f"+ {s['type']}: {s['name']}"
                    if len(sub_text) > 30:
                        sub_text = sub_text[:28] + "…"
                    link.add(
                        Text(
                            sub_text,
                            insert=(nx + 10, cursor_y),
                            fill=f"#{color_cfg['accent']}",
                            class_="node-detail",
                        )
                    )
                    cursor_y += 16

            nodes_group.add(link)

        drawing.add(nodes_group)
        return drawing
