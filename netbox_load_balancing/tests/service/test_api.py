from utilities.testing import APIViewTestCases
from netbox_load_balancing.tests.custom import (
    APITestCase,
    NetBoxLoadBalancingGraphQLMixin,
)
from netbox_load_balancing.models import LBService


class LBServiceAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxLoadBalancingGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = LBService

    brief_fields = [
        "description",
        "disabled",
        "display",
        "id",
        "name",
        "reference",
        "url",
    ]

    create_data = [
        {"name": "service-1", "reference": "1.1.1.1/32", "disabled": False},
        {"name": "service-2", "reference": "1.1.1.2/32", "disabled": False},
        {"name": "service-3", "reference": "1.1.1.3/32", "disabled": True},
    ]

    bulk_update_data = {
        "description": "Test Service",
    }
    bulk_update_invalid_data = {
        "disabled": "invalid_disabled",
    }

    @classmethod
    def setUpTestData(cls):
        services = (
            LBService(name="service-4", reference="1.1.1.4/32", disabled=True),
            LBService(name="service-5", reference="1.1.1.5/32", disabled=True),
            LBService(name="service-6", reference="1.1.1.6/32", disabled=False),
        )
        LBService.objects.bulk_create(services)
