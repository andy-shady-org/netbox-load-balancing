from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from utilities.testing import ChangeLoggedFilterSetTests
from ipam.models import Prefix, IPAddress, IPRange

from netbox_load_balancing.models import (
    VirtualIP,
    VirtualIPPool,
    VirtualIPPoolAssignment,
)
from netbox_load_balancing.filtersets import VirtualIPFilterSet


class VirtualIPFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = VirtualIP.objects.all()
    filterset = VirtualIPFilterSet

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

        cls.vips = (
            VirtualIP(
                name="virtual-ip-1",
                virtual_pool=cls.pools[0],
                address=cls.addresses[0],
                dns_name="test4.example.com",
                disabled=True,
                route_health_injection=False,
            ),
            VirtualIP(
                name="virtual-ip-2",
                virtual_pool=cls.pools[0],
                address=cls.addresses[1],
                dns_name="test4.example.com",
                disabled=True,
                route_health_injection=False,
            ),
            VirtualIP(
                name="virtual-ip-3",
                virtual_pool=cls.pools[1],
                address=cls.addresses[2],
                dns_name="test5.example.com",
                disabled=True,
                route_health_injection=False,
            ),
            VirtualIP(
                name="virtual-ip-4",
                virtual_pool=cls.pools[2],
                address=cls.addresses[3],
                dns_name="test6.example.com",
                disabled=False,
                route_health_injection=False,
            ),
        )
        VirtualIP.objects.bulk_create(cls.vips)

    def test_name(self):
        params = {"name": ["virtual-ip-1", "virtual-ip-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_disabled(self):
        params = {"disabled": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"disabled": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_addresses(self):
        params = {
            "address_id": [
                self.addresses[0].pk,
                self.addresses[1].pk,
                self.addresses[2].pk,
                self.addresses[3].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 4)
        params = {"address": [str(self.addresses[0].address)]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address": [str(self.addresses[1].address)]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address": [str(self.addresses[2].address)]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address": [str(self.addresses[3].address)]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_virtual_pool(self):
        params = {"virtual_pool_id": [self.pools[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"virtual_pool": [self.pools[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"virtual_pool_id": [self.pools[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"virtual_pool": [self.pools[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
