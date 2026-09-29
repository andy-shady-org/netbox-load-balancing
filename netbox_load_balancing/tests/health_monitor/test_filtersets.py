from django.test import TestCase

from utilities.testing import ChangeLoggedFilterSetTestMixin
from tenancy.models import Tenant, TenantGroup

from netbox_load_balancing.models import HealthMonitor
from netbox_load_balancing.filtersets import HealthMonitorFilterSet
from netbox_load_balancing.choices import (
    HealthMonitorTypeChoices,
)


class HealthMonitorFiterSetTestCase(TestCase, ChangeLoggedFilterSetTestMixin):
    queryset = HealthMonitor.objects.all()
    filterset = HealthMonitorFilterSet

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

        cls.monitors = (
            HealthMonitor(
                name="monitor-4",
                type=HealthMonitorTypeChoices.PING,
                monitor_port=10,
                http_response_codes=[200, 201],
                disabled=True,
                tenant=cls.tenants[0],
            ),
            HealthMonitor(
                name="monitor-5",
                type=HealthMonitorTypeChoices.HTTP,
                monitor_port=10,
                http_response_codes=[200, 201],
                disabled=True,
                tenant=cls.tenants[1],
            ),
            HealthMonitor(
                name="monitor-6",
                type=HealthMonitorTypeChoices.HTTP,
                monitor_port=10,
                http_response_codes=[200, 201],
                disabled=False,
                tenant=cls.tenants[2],
            ),
        )
        HealthMonitor.objects.bulk_create(cls.monitors)

    def test_name(self):
        params = {"name": ["monitor-4", "monitor-5"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant(self):
        params = {"tenant_id": [self.tenants[0].pk, self.tenants[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"tenant": [self.tenants[0].slug, self.tenants[1].slug]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_defaults(self):
        params = {"type": [HealthMonitorTypeChoices.PING]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"type": [HealthMonitorTypeChoices.HTTP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_disabled(self):
        params = {"disabled": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"disabled": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
