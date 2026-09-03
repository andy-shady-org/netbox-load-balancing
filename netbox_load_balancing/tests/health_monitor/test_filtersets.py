from django.test import TestCase

from utilities.testing import ChangeLoggedFilterSetTestMixin

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
        cls.monitors = (
            HealthMonitor(
                name="monitor-4",
                type=HealthMonitorTypeChoices.PING,
                monitor_port=10,
                http_response_codes=[200, 201],
                disabled=True,
            ),
            HealthMonitor(
                name="monitor-5",
                type=HealthMonitorTypeChoices.HTTP,
                monitor_port=10,
                http_response_codes=[200, 201],
                disabled=True,
            ),
            HealthMonitor(
                name="monitor-6",
                type=HealthMonitorTypeChoices.HTTP,
                monitor_port=10,
                http_response_codes=[200, 201],
                disabled=False,
            ),
        )
        HealthMonitor.objects.bulk_create(cls.monitors)

    def test_name(self):
        params = {"name": ["monitor-4", "monitor-5"]}
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
