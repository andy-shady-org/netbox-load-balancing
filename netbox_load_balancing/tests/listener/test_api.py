from utilities.testing import APIViewTestCases
from netbox_load_balancing.tests.custom import (
    APITestCase,
    NetBoxLoadBalancingGraphQLMixin,
)
from netbox_load_balancing.models import Listener, LBService


class ListenerAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxLoadBalancingGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Listener

    brief_fields = ["description", "display", "id", "name", "port", "url"]

    bulk_update_data = {
        "description": "Test Service",
    }
    bulk_update_invalid_data = {
        "service": "invalid_service",
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

        cls.create_data = [
            {"name": "listener-4", "service": cls.services[0].pk, "port": 1},
            {"name": "listener-5", "service": cls.services[1].pk, "port": 1},
            {"name": "listener-6", "service": cls.services[2].pk, "port": 1},
        ]
