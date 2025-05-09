from django.test import TestCase

from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_load_balancing.models import VirtualIPPool
from netbox_load_balancing.filtersets import VirtualIPPoolFilterSet


class VirtualIPPoolFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = VirtualIPPool.objects.all()
    filterset = VirtualIPPoolFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.tenant_groups = (
            TenantGroup(name="Tenant group 1", slug="tenant-group-1"),
            TenantGroup(name="Tenant group 2", slug="tenant-group-2"),
            TenantGroup(name="Tenant group 3", slug="tenant-group-3"),
        )
        for tenantgroup in cls.tenant_groups:
            tenantgroup.save()

        cls.tenants = (
            Tenant(name="Tenant 1", slug="tenant-1", group=cls.tenant_groups[0]),
            Tenant(name="Tenant 2", slug="tenant-2", group=cls.tenant_groups[1]),
            Tenant(name="Tenant 3", slug="tenant-3", group=cls.tenant_groups[2]),
        )
        Tenant.objects.bulk_create(cls.tenants)

        cls.pools = (
            VirtualIPPool(
                name="virtual-pool-4",
                disabled=True,
                tenant=cls.tenants[0],
            ),
            VirtualIPPool(
                name="virtual-pool-5",
                disabled=True,
                tenant=cls.tenants[1],
            ),
            VirtualIPPool(
                name="virtual-pool-6",
                disabled=False,
                tenant=cls.tenants[2],
            ),
        )
        for pool in cls.pools:
            pool.save()

    def test_name(self):
        params = {"name": ["virtual-pool-4", "virtual-pool-5"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant(self):
        params = {"tenant_id": [self.tenants[0].pk, self.tenants[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"tenant": [self.tenants[0].slug, self.tenants[1].slug]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant_group(self):
        params = {
            "tenant_group_id": [self.tenant_groups[0].pk, self.tenant_groups[1].pk]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "tenant_group": [self.tenant_groups[0].slug, self.tenant_groups[1].slug]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_disabled(self):
        params = {"disabled": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"disabled": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
