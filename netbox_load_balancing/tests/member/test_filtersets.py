from django.test import TestCase

from utilities.testing import ChangeLoggedFilterSetTestMixin

from ipam.models import IPAddress

from netbox_load_balancing.models import Member
from netbox_load_balancing.filtersets import MemberFilterSet


class MemberFiterSetTestCase(TestCase, ChangeLoggedFilterSetTestMixin):
    queryset = Member.objects.all()
    filterset = MemberFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.addresses = (
            IPAddress(
                address="1.1.1.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.2.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.3.1/24",
                status="active",
            ),
        )
        IPAddress.objects.bulk_create(cls.addresses)

        members = (
            Member(
                name="member-1",
                reference="1.1.1.4/32",
                disabled=True,
                ip_address=cls.addresses[0],
            ),
            Member(
                name="member-2",
                reference="1.1.1.5/32",
                disabled=True,
                ip_address=cls.addresses[1],
            ),
            Member(
                name="member-3",
                reference="1.1.1.6/32",
                disabled=False,
                ip_address=cls.addresses[2],
            ),
        )
        Member.objects.bulk_create(members)

    def test_name(self):
        params = {"name": ["member-2", "member-1"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_addresses(self):
        params = {"ip_address_id": [self.addresses[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ip_address_id": [self.addresses[0].pk, self.addresses[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "ip_address_id": [
                self.addresses[0].pk,
                self.addresses[1].pk,
                self.addresses[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"ip_address": [str(self.addresses[0].address)]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_disabled(self):
        params = {"disabled": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"disabled": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
