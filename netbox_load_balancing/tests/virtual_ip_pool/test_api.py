from utilities.testing import APIViewTestCases
from netbox_load_balancing.tests.custom import (
    APITestCase,
    NetBoxLoadBalancingGraphQLMixin,
)
from netbox_load_balancing.models import VirtualIPPool


class VirtualIPPoolAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxLoadBalancingGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = VirtualIPPool

    brief_fields = [
        "description",
        "disabled",
        "display",
        "id",
        "name",
        "url",
    ]

    create_data = [
        {"name": "virtual-pool-1", "disabled": False},
        {"name": "virtual-pool-2", "disabled": False},
        {"name": "virtual-pool-3", "disabled": True},
    ]

    bulk_update_data = {
        "description": "Test Service",
    }
    bulk_update_invalid_data = {
        "disabled": "invalid_disabled",
    }

    @classmethod
    def setUpTestData(cls):
        pools = (
            VirtualIPPool(name="virtual-pool-4", disabled=True),
            VirtualIPPool(name="virtual-pool-5", disabled=True),
            VirtualIPPool(name="virtual-pool-6", disabled=False),
        )
        VirtualIPPool.objects.bulk_create(pools)
