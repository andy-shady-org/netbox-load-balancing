from django.test import TestCase

from utilities.testing import ChangeLoggedFilterSetTests

from netbox_load_balancing.models import LBService, Pool, Listener
from netbox_load_balancing.filtersets import PoolFilterSet
from netbox_load_balancing.choices import (
    PoolAlgorythmChoices,
    PoolSessionPersistenceChoices,
    PoolBackupSessionPersistenceChoices,
)


class PoolFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = Pool.objects.all()
    filterset = PoolFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.services = (
            LBService(name="service-1", reference="1.1.1.4/32", disabled=True),
            LBService(name="service-2", reference="1.1.1.5/32", disabled=True),
            LBService(name="service-3", reference="1.1.1.6/32", disabled=True),
        )
        LBService.objects.bulk_create(cls.services)

        cls.listeners = (
            Listener(name="listener-1", service=cls.services[0], port=10),
            Listener(name="listener-2", service=cls.services[1], port=10),
            Listener(name="listener-3", service=cls.services[2], port=10),
        )
        Listener.objects.bulk_create(cls.listeners)

        cls.pools = (
            Pool(
                name="pool-1",
                member_port=1,
                disabled=True,
                backup_persistence=PoolBackupSessionPersistenceChoices.SOURCE_IP,
            ),
            Pool(
                name="pool-2",
                member_port=2,
                disabled=True,
                algorythm=PoolAlgorythmChoices.ROUND_ROBIN,
            ),
            Pool(
                name="pool-3",
                member_port=2,
                disabled=False,
                session_persistence=PoolSessionPersistenceChoices.SSL_BRIDGE,
            ),
        )
        Pool.objects.bulk_create(cls.pools)
        cls.pools[0].listeners.add(cls.listeners[0])
        cls.pools[1].listeners.set([cls.listeners[1], cls.listeners[2]])
        cls.pools[2].listeners.set(cls.listeners)

    def test_name(self):
        params = {"name": ["pool-1", "pool-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_disabled(self):
        params = {"disabled": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"disabled": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_listeners(self):
        params = {"listener_id": [self.listeners[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"listener_id": [self.listeners[1].pk, self.listeners[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "listener_id": [
                self.listeners[0].pk,
                self.listeners[1].pk,
                self.services[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"listener": [self.listeners[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"listener": [self.listeners[0].name, self.listeners[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_algorythm(self):
        params = {"algorythm": [PoolAlgorythmChoices.LEAST_CONNECTION]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"algorythm": [PoolAlgorythmChoices.ROUND_ROBIN]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_backup_persistence(self):
        params = {"backup_persistence": [PoolBackupSessionPersistenceChoices.NONE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"backup_persistence": [PoolBackupSessionPersistenceChoices.SOURCE_IP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_session_persistence(self):
        params = {"session_persistence": [PoolSessionPersistenceChoices.SOURCE_IP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"session_persistence": [PoolSessionPersistenceChoices.SSL_BRIDGE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_persistence_timeout(self):
        params = {"persistence_timeout": [0]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_backup_timeout(self):
        params = {"backup_timeout": [0]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_member_port(self):
        params = {"member_port": [1]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"member_port": [2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
