from django.test import TestCase

from utilities.testing import ChangeLoggedFilterSetTestMixin

from netbox_load_balancing.models import Listener, LBService, Pool
from netbox_load_balancing.filtersets import ListenerFilterSet
from netbox_load_balancing.choices import ListenerProtocolChoices


class ListenerFiterSetTestCase(TestCase, ChangeLoggedFilterSetTestMixin):
    queryset = Listener.objects.all()
    filterset = ListenerFilterSet

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
            Listener(
                name="listener-3",
                service=cls.services[2],
                port=10,
                protocol=ListenerProtocolChoices.HTTP,
            ),
        )
        Listener.objects.bulk_create(cls.listeners)

        cls.pools = (
            Pool(
                name="pool-test-1",
                member_port=1,
            ),
        )
        Pool.objects.bulk_create(cls.pools)
        cls.pools[0].listeners.add(cls.listeners[0])

    def test_name(self):
        params = {"name": ["listener-1", "listener-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_services(self):
        params = {"service_id": [self.services[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"service_id": [self.services[0].pk, self.services[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "service_id": [
                self.services[0].pk,
                self.services[1].pk,
                self.services[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"service": [self.services[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"pool_id": [self.pools[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_defaults(self):
        params = {"protocol": [ListenerProtocolChoices.TCP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"protocol": [ListenerProtocolChoices.HTTP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
