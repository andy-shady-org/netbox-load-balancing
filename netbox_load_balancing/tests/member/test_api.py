from utilities.testing import APIViewTestCases
from ipam.models import IPAddress
from netbox_load_balancing.tests.custom import (
    APITestCase,
    NetBoxLoadBalancingGraphQLMixin,
)
from netbox_load_balancing.models import Member


class MemberAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxLoadBalancingGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Member

    brief_fields = [
        "description",
        "disabled",
        "display",
        "id",
        "name",
        "reference",
        "url",
    ]

    bulk_update_data = {
        "description": "Test Service",
    }
    bulk_update_invalid_data = {
        "ip_address": "invalid_ip_address",
    }

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
                name="member-4",
                reference="1.1.1.4/32",
                disabled=True,
                ip_address=cls.addresses[0],
            ),
            Member(
                name="member-5",
                reference="1.1.1.5/32",
                disabled=True,
                ip_address=cls.addresses[1],
            ),
            Member(
                name="member-6",
                reference="1.1.1.6/32",
                disabled=False,
                ip_address=cls.addresses[2],
            ),
        )
        Member.objects.bulk_create(members)

        cls.create_data = [
            {
                "name": "member-1",
                "reference": "1.1.1.1/32",
                "disabled": False,
                "ip_address": cls.addresses[0].pk,
            },
            {
                "name": "member-2",
                "reference": "1.1.1.2/32",
                "disabled": False,
                "ip_address": cls.addresses[1].pk,
            },
            {
                "name": "member-3",
                "reference": "1.1.1.3/32",
                "disabled": True,
                "ip_address": cls.addresses[2].pk,
            },
        ]
