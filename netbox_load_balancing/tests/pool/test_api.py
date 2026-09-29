from utilities.testing import APIViewTestCases
from netbox_load_balancing.tests.custom import (
    APITestCase,
    NetBoxLoadBalancingGraphQLMixin,
)
from netbox_load_balancing.models import Pool, Listener, LBService


class PoolAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxLoadBalancingGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Pool

    brief_fields = ["description", "disabled", "display", "id", "name", "url"]

    bulk_update_data = {
        "description": "Test Service",
    }
    bulk_update_invalid_data = {
        "member_port": "invalid_port",
    }

    @classmethod
    def setUpTestData(cls):
        cls.services = (
            LBService(name="service-1", reference="1.1.1.4/32", disabled=True),
            LBService(name="service-2", reference="1.1.1.5/32", disabled=True),
            LBService(name="service-3", reference="1.1.1.6/32", disabled=False),
        )
        LBService.objects.bulk_create(cls.services)
        cls.listeners = (
            Listener(name="listener-1", service=cls.services[0], port=10),
            Listener(name="listener-2", service=cls.services[1], port=10),
            Listener(name="listener-3", service=cls.services[2], port=10),
        )
        Listener.objects.bulk_create(cls.listeners)
        pools = (
            Pool(name="pool-4", member_port=1, disabled=True),
            Pool(name="pool-5", member_port=2, disabled=True),
            Pool(name="pool-6", member_port=3, disabled=False),
        )
        Pool.objects.bulk_create(pools)
        for p in pools:
            p.listeners.set(cls.listeners)

        cls.create_data = [
            {
                "name": "pool-1",
                "member_port": 1,
                "disabled": False,
                "listeners": [cls.listeners[0].pk, cls.listeners[1].pk],
            },
            {
                "name": "pool-2",
                "member_port": 2,
                "disabled": False,
                "listeners": [cls.listeners[0].pk, cls.listeners[1].pk],
            },
            {
                "name": "pool-3",
                "member_port": 3,
                "disabled": True,
                "listeners": [cls.listeners[0].pk, cls.listeners[1].pk],
            },
        ]
