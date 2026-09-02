from django.test import TestCase
from netaddr import IPNetwork

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site, VirtualDeviceContext
from ipam.models import IPAddress, IPRange, Prefix, VLAN
from virtualization.models import Cluster, ClusterType, VirtualMachine

from netbox_load_balancing.models import (
    LBService,
    LBServiceAssignment,
    VirtualIP,
    VirtualIPPool,
    VirtualIPPoolAssignment,
    Listener,
    Pool,
    HealthMonitor,
    HealthMonitorAssignment,
    Member,
    MemberAssignment,
)
from netbox_load_balancing.svg.diagram import LBServiceDiagramSVG, get_lbservice_hierarchy_data


class LBServiceDiagramTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 1. Base LB Service
        cls.service = LBService.objects.create(
            name="Web-LB-Service",
            reference="SVC-001",
        )

        # 2. Infra Objects
        cls.site = Site.objects.create(name="Site 1", slug="site-1")
        cls.manufacturer = Manufacturer.objects.create(name="Cisco", slug="cisco")
        cls.device_type = DeviceType.objects.create(
            manufacturer=cls.manufacturer, model="CSR1000v", slug="csr1000v"
        )
        cls.role = DeviceRole.objects.create(name="Router", slug="router")
        cls.device = Device.objects.create(
            name="Edge-Router-01",
            site=cls.site,
            device_type=cls.device_type,
            role=cls.role,
        )

        cls.cluster_type = ClusterType.objects.create(name="VMware", slug="vmware")
        cls.cluster = Cluster.objects.create(name="Cluster 1", type=cls.cluster_type)
        cls.vm = VirtualMachine.objects.create(
            name="LB-VM-01",
            cluster=cls.cluster,
        )

        cls.vdc = VirtualDeviceContext.objects.create(
            name="VDC-Primary",
            device=cls.device,
        )

        # 3. IPAM & VIP Pool
        cls.vip_pool = VirtualIPPool.objects.create(name="Public-VIP-Pool")
        cls.prefix = Prefix.objects.create(prefix="198.51.100.0/24")
        cls.vlan = VLAN.objects.create(vid=100, name="DMZ-VLAN")
        cls.ip_range = IPRange.objects.create(
            start_address=IPNetwork("198.51.100.10/24"),
            end_address=IPNetwork("198.51.100.50/24"),
        )

        VirtualIPPoolAssignment.objects.create(
            virtual_pool=cls.vip_pool,
            assigned_object=cls.prefix,
        )
        VirtualIPPoolAssignment.objects.create(
            virtual_pool=cls.vip_pool,
            assigned_object=cls.vlan,
        )
        VirtualIPPoolAssignment.objects.create(
            virtual_pool=cls.vip_pool,
            assigned_object=cls.ip_range,
        )

        cls.ip_vip = IPAddress.objects.create(address="198.51.100.20/24")
        cls.vip = VirtualIP.objects.create(
            name="Web-VIP",
            virtual_pool=cls.vip_pool,
            address=cls.ip_vip,
            dns_name="web.example.com",
        )

        # Assign infra & VIP to service
        LBServiceAssignment.objects.create(service=cls.service, assigned_object=cls.device)
        LBServiceAssignment.objects.create(service=cls.service, assigned_object=cls.vm)
        LBServiceAssignment.objects.create(service=cls.service, assigned_object=cls.vdc)
        LBServiceAssignment.objects.create(service=cls.service, assigned_object=cls.vip)

        # 4. Southbound: Listeners, Pools, Monitors, Members
        cls.listener_http = Listener.objects.create(
            name="HTTP-80",
            service=cls.service,
            port=80,
            protocol="http",
        )
        cls.listener_https = Listener.objects.create(
            name="HTTPS-443",
            service=cls.service,
            port=443,
            protocol="https",
        )

        cls.pool = Pool.objects.create(
            name="Web-Backend-Pool",
            algorythm="round-robin",
            session_persistence="source-ip",
        )
        cls.pool.listeners.add(cls.listener_http, cls.listener_https)

        cls.monitor = HealthMonitor.objects.create(
            name="HTTP-Health-Check",
            type="http",
            monitor_url="/healthz",
            http_version="1.1",
        )
        HealthMonitorAssignment.objects.create(
            monitor=cls.monitor,
            assigned_object=cls.pool,
        )

        cls.member_ip_1 = IPAddress.objects.create(address="10.0.0.11/24")
        cls.member_ip_2 = IPAddress.objects.create(address="10.0.0.12/24")

        cls.member_1 = Member.objects.create(
            name="Web-Srv-01",
            ip_address=cls.member_ip_1,
            reference="SRV-01",
        )
        cls.member_2 = Member.objects.create(
            name="Web-Srv-02",
            ip_address=cls.member_ip_2,
            reference="SRV-02",
        )

        MemberAssignment.objects.create(
            member=cls.member_1,
            assigned_object=cls.pool,
            weight=1,
        )
        MemberAssignment.objects.create(
            member=cls.member_2,
            assigned_object=cls.pool,
            weight=2,
        )

    def test_get_lbservice_hierarchy_data(self):
        data = get_lbservice_hierarchy_data(self.service)

        # Verify Service
        self.assertEqual(data["service"]["name"], "Web-LB-Service")
        self.assertEqual(data["service"]["reference"], "SVC-001")

        # Verify Northbound Infra
        infra_types = [item["type"] for item in data["infra"]]
        self.assertIn("Device", infra_types)
        self.assertIn("Virtual Machine", infra_types)
        self.assertIn("VDC", infra_types)

        # Verify VIPs & VIP Pool
        self.assertEqual(len(data["vips"]), 1)
        self.assertEqual(data["vips"][0]["name"], "Web-VIP")
        self.assertEqual(data["vips"][0]["dns_name"], "web.example.com")
        self.assertIn(f"vippool_{self.vip_pool.pk}", data["vip_pools"])

        # Verify Listeners
        listener_names = [l["name"] for l in data["listeners"]]
        self.assertIn("HTTP-80", listener_names)
        self.assertIn("HTTPS-443", listener_names)

        # Verify Pool
        self.assertEqual(len(data["pools"]), 1)
        self.assertEqual(data["pools"][0]["name"], "Web-Backend-Pool")

        # Verify Health Monitor
        self.assertEqual(len(data["health_monitors"]), 1)
        self.assertEqual(data["health_monitors"][0]["name"], "HTTP-Health-Check")

        # Verify Members
        member_names = [m["name"] for m in data["members"]]
        self.assertIn("Web-Srv-01", member_names)
        self.assertIn("Web-Srv-02", member_names)

        # Verify Edges
        edge_sources = [e["source"] for e in data["edges"]]
        edge_targets = [e["target"] for e in data["edges"]]
        self.assertIn(f"service_{self.service.pk}", edge_sources)
        self.assertIn(f"service_{self.service.pk}", edge_targets)

    def test_diagram_svg_render(self):
        diagram = LBServiceDiagramSVG(self.service, base_url="http://netbox.local")
        drawing = diagram.render()
        svg_xml = drawing.tostring()

        # Check SVG tags and content
        self.assertIn("<svg", svg_xml)
        self.assertIn("Web-LB-Service", svg_xml)
        self.assertIn("Web-VIP", svg_xml)
        self.assertIn("Public-VIP-Pool", svg_xml)
        self.assertIn("HTTP-80", svg_xml)
        self.assertIn("Web-Backend-Pool", svg_xml)
        self.assertIn("HTTP-Health-Check", svg_xml)
        self.assertIn("Web-Srv-01", svg_xml)

        # Check hyperlinks exist
        self.assertIn(self.service.get_absolute_url(), svg_xml)
        self.assertIn(self.vip.get_absolute_url(), svg_xml)
        self.assertIn(self.pool.get_absolute_url(), svg_xml)
        self.assertIn(self.listener_http.get_absolute_url(), svg_xml)
        self.assertIn(self.monitor.get_absolute_url(), svg_xml)
        self.assertIn(self.member_1.get_absolute_url(), svg_xml)

    def test_empty_service_diagram(self):
        empty_service = LBService.objects.create(
            name="Empty-Service",
            reference="EMPTY-001",
        )
        diagram = LBServiceDiagramSVG(empty_service)
        drawing = diagram.render()
        svg_xml = drawing.tostring()

        self.assertIn("<svg", svg_xml)
        self.assertIn("Empty-Service", svg_xml)
