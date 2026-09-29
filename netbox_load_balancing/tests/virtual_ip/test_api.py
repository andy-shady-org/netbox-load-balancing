from django.contrib.contenttypes.models import ContentType
from utilities.testing import APIViewTestCases
from netbox_load_balancing.tests.custom import (
    APITestCase,
    NetBoxLoadBalancingGraphQLMixin,
)
from ipam.models import Prefix, IPAddress, IPRange
from netbox_load_balancing.models import (
    VirtualIP,
    VirtualIPPool,
    VirtualIPPoolAssignment,
)


class VirtualIPAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxLoadBalancingGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = VirtualIP

    brief_fields = [
        "description",
        "disabled",
        "display",
        "dns_name",
        "id",
        "name",
        "route_health_injection",
        "url",
    ]

    bulk_update_data = {
        "description": "Test Virtual IP",
    }
    bulk_update_invalid_data = {
        "disabled": "invalid_disabled",
    }

    @classmethod
    def setUpTestData(cls):
        cls.prefixes = (
            Prefix(prefix="10.1.1.0/24", status="active"),
            Prefix(prefix="10.1.2.0/24", status="active"),
        )
        Prefix.objects.bulk_create(cls.prefixes)

        cls.ip_ranges = (
            IPRange(start_address="10.1.3.1/24", end_address="10.1.3.254/24", size=253),
        )
        IPRange.objects.bulk_create(cls.ip_ranges)

        cls.addresses = (
            IPAddress(address="10.1.1.1/24", status="active"),
            IPAddress(address="10.1.1.2/24", status="active"),
            IPAddress(address="10.1.3.1/24", status="active"),
            IPAddress(address="10.1.3.2/24", status="active"),
            IPAddress(address="10.1.3.3/24", status="active"),
        )
        IPAddress.objects.bulk_create(cls.addresses)

        cls.pools = (
            VirtualIPPool(name="virtual-pool-4", disabled=False),
            VirtualIPPool(name="virtual-pool-5", disabled=False),
            VirtualIPPool(name="virtual-pool-6", disabled=False),
        )
        VirtualIPPool.objects.bulk_create(cls.pools)

        cls.assignments = (
            VirtualIPPoolAssignment(
                virtual_pool=cls.pools[0],
                assigned_object=cls.prefixes[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "ipam", "prefix"
                ),
                assigned_object_id=cls.prefixes[0].pk,
                weight=5,
                disabled=False,
            ),
            VirtualIPPoolAssignment(
                virtual_pool=cls.pools[0],
                assigned_object=cls.prefixes[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "ipam", "prefix"
                ),
                assigned_object_id=cls.prefixes[1].pk,
                weight=1,
                disabled=True,
            ),
            VirtualIPPoolAssignment(
                virtual_pool=cls.pools[1],
                assigned_object=cls.prefixes[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "ipam", "prefix"
                ),
                assigned_object_id=cls.prefixes[0].pk,
                weight=1,
                disabled=False,
            ),
            VirtualIPPoolAssignment(
                virtual_pool=cls.pools[2],
                assigned_object=cls.ip_ranges[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "ipam", "iprange"
                ),
                assigned_object_id=cls.ip_ranges[0].pk,
                weight=1,
                disabled=False,
            ),
        )
        VirtualIPPoolAssignment.objects.bulk_create(cls.assignments)

        cls.create_data = [
            {
                "name": "virtual-ip-1",
                "virtual_pool": cls.pools[0].pk,
                "dns_name": "test1.example.com",
                "disabled": False,
                "route_health_injection": False,
            },
            {
                "name": "virtual-ip-2",
                "virtual_pool": cls.pools[2].pk,
                "address": cls.addresses[4].pk,
                "dns_name": "test2.example.com",
                "disabled": False,
                "route_health_injection": False,
            },
            {
                "name": "virtual-ip-3",
                "virtual_pool": cls.pools[2].pk,
                "dns_name": "test3.example.com",
                "disabled": True,
                "route_health_injection": True,
            },
        ]

        cls.vips = (
            VirtualIP(
                name="virtual-ip-4",
                virtual_pool=cls.pools[0],
                address=cls.addresses[0],
                dns_name="test4.example.com",
                disabled=True,
                route_health_injection=False,
            ),
            VirtualIP(
                name="virtual-ip-5",
                virtual_pool=cls.pools[0],
                address=cls.addresses[1],
                dns_name="test4.example.com",
                disabled=True,
                route_health_injection=False,
            ),
            VirtualIP(
                name="virtual-ip-6",
                virtual_pool=cls.pools[1],
                address=cls.addresses[2],
                dns_name="test5.example.com",
                disabled=True,
                route_health_injection=False,
            ),
            VirtualIP(
                name="virtual-ip-7",
                virtual_pool=cls.pools[2],
                address=cls.addresses[3],
                dns_name="test6.example.com",
                disabled=False,
                route_health_injection=False,
            ),
        )
        VirtualIP.objects.bulk_create(cls.vips)

    def test_addresses(self):
        self.assertEqual(str(self.vips[0].address), "10.1.1.1/24")
        self.assertEqual(str(self.vips[1].address), "10.1.1.2/24")
        self.assertEqual(str(self.vips[2].address), "10.1.3.1/24")
        self.assertEqual(str(self.vips[3].address), "10.1.3.2/24")

    def test_disabled(self):
        self.assertTrue(self.vips[0].disabled)
        self.assertTrue(self.vips[1].disabled)
        self.assertTrue(self.vips[2].disabled)
        self.assertFalse(self.vips[3].disabled)
