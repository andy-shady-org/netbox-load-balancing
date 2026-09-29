from utilities.testing import APIViewTestCases
from netbox_load_balancing.tests.custom import (
    APITestCase,
    NetBoxLoadBalancingGraphQLMixin,
)
from netbox_load_balancing.models import HealthMonitor
from netbox_load_balancing.choices import (
    HealthMonitorTypeChoices,
)


class HealthMonitorAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxLoadBalancingGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = HealthMonitor

    brief_fields = ["description", "disabled", "display", "id", "name", "type", "url"]

    create_data = [
        {
            "name": "monitor-1",
            "type": HealthMonitorTypeChoices.HTTP,
            "monitor_port": 10,
            "http_response_codes": [200, 201],
            "disabled": False,
        },
        {
            "name": "monitor-2",
            "type": HealthMonitorTypeChoices.TCP,
            "monitor_port": 10,
            "http_response_codes": [200, 201],
            "disabled": False,
        },
        {
            "name": "monitor-3",
            "type": HealthMonitorTypeChoices.PING,
            "monitor_port": 10,
            "http_response_codes": [200, 201],
            "disabled": True,
        },
    ]

    bulk_update_data = {
        "description": "Test Monitor",
    }
    bulk_update_invalid_data = {
        "type": "invalid_type",
    }

    @classmethod
    def setUpTestData(cls):
        monitors = (
            HealthMonitor(
                name="monitor-4",
                type=HealthMonitorTypeChoices.HTTP,
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
        HealthMonitor.objects.bulk_create(monitors)
