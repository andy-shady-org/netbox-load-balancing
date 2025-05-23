# Generated by Django 5.1.7 on 2025-04-13 06:47

import django.contrib.postgres.fields
import django.core.validators
import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0123_journalentry_kind_default"),
        ("ipam", "0076_natural_ordering"),
        ("tenancy", "0017_natural_ordering"),
    ]

    operations = [
        migrations.CreateModel(
            name="HealthMonitor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                ("comments", models.TextField(blank=True)),
                ("name", models.CharField(max_length=255)),
                ("template", models.CharField(blank=True, max_length=255, null=True)),
                ("type", models.CharField(default="http", max_length=255)),
                (
                    "monitor_url",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "http_response",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "monitor_host",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "monitor_port",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(65534),
                        ],
                    ),
                ),
                ("http_version", models.CharField(default="1.0", max_length=255)),
                ("http_secure", models.BooleanField(default=False)),
                (
                    "http_response_codes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.PositiveIntegerField(
                            default=200,
                            validators=[
                                django.core.validators.MinValueValidator(100),
                                django.core.validators.MaxValueValidator(599),
                            ],
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("probe_interval", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "response_timeout",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("disabled", models.BooleanField(default=False)),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "verbose_name": "Health Monitor",
                "verbose_name_plural": "Health Monitors",
                "ordering": ("name",),
                "unique_together": {("name", "template")},
            },
        ),
        migrations.CreateModel(
            name="LBService",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                ("comments", models.TextField(blank=True)),
                ("name", models.CharField(max_length=255)),
                ("reference", models.CharField(max_length=255)),
                ("disabled", models.BooleanField(default=False)),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_related",
                        to="tenancy.tenant",
                    ),
                ),
            ],
            options={
                "verbose_name": "LB Service",
                "verbose_name_plural": "LB Services",
                "ordering": ("name", "reference"),
                "unique_together": {("name", "reference")},
            },
        ),
        migrations.CreateModel(
            name="Listener",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                ("comments", models.TextField(blank=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "port",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(65534),
                        ]
                    ),
                ),
                ("protocol", models.CharField(default="tcp", max_length=255)),
                ("source_nat", models.BooleanField(default=True)),
                ("use_proxy_port", models.BooleanField(default=False)),
                (
                    "max_clients",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(4294967295),
                        ],
                    ),
                ),
                (
                    "max_requests",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(4294967295),
                        ],
                    ),
                ),
                (
                    "client_timeout",
                    models.IntegerField(
                        default=9000,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(31536000),
                        ],
                    ),
                ),
                (
                    "server_timeout",
                    models.IntegerField(
                        default=9000,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(31536000),
                        ],
                    ),
                ),
                ("client_keepalive", models.BooleanField(default=False)),
                ("surge_protection", models.BooleanField(default=False)),
                ("tcp_buffering", models.BooleanField(default=False)),
                ("compression", models.BooleanField(default=False)),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_service",
                        to="netbox_load_balancing.lbservice",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "verbose_name": "Listener",
                "verbose_name_plural": "Listeners",
                "ordering": ("name", "port"),
                "unique_together": {("name", "service")},
            },
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                ("comments", models.TextField(blank=True)),
                ("name", models.CharField(max_length=255)),
                ("reference", models.CharField(max_length=255)),
                ("disabled", models.BooleanField(default=False)),
                (
                    "ip_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_members",
                        to="ipam.ipaddress",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "verbose_name": "Member",
                "verbose_name_plural": "Member",
                "ordering": ("name", "ip_address"),
                "unique_together": {("ip_address", "name")},
            },
        ),
        migrations.CreateModel(
            name="Pool",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                ("comments", models.TextField(blank=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "algorythm",
                    models.CharField(default="least-connection", max_length=255),
                ),
                (
                    "session_persistence",
                    models.CharField(default="source-ip", max_length=255),
                ),
                (
                    "backup_persistence",
                    models.CharField(default="None", max_length=255),
                ),
                (
                    "persistence_timeout",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1440),
                        ],
                    ),
                ),
                (
                    "backup_timeout",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1440),
                        ],
                    ),
                ),
                (
                    "member_port",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(65535),
                        ],
                    ),
                ),
                ("disabled", models.BooleanField(default=False)),
                (
                    "listeners",
                    models.ManyToManyField(
                        blank=True,
                        related_name="%(class)s_listeners",
                        to="netbox_load_balancing.listener",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "verbose_name": "Pool",
                "verbose_name_plural": "Pools",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="HealthMonitorAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("assigned_object_id", models.PositiveBigIntegerField()),
                ("disabled", models.BooleanField(default=False)),
                (
                    "weight",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(32767),
                        ],
                    ),
                ),
                (
                    "assigned_object_type",
                    models.ForeignKey(
                        limit_choices_to=models.Q(
                            models.Q(
                                ("app_label", "netbox_load_balancing"),
                                ("model", "pool"),
                            )
                        ),
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "monitor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="netbox_load_balancing.healthmonitor",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "verbose_name": "LB Health Monitor Assignment",
                "verbose_name_plural": "LB Health Monitor Assignments",
                "indexes": [
                    models.Index(
                        fields=["assigned_object_type", "assigned_object_id"],
                        name="netbox_load_assigne_8f7c2e_idx",
                    )
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=(
                            "assigned_object_type",
                            "assigned_object_id",
                            "monitor",
                        ),
                        name="netbox_load_balancing_healthmonitorassignment_unique_monitor",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="LBServiceAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("assigned_object_id", models.PositiveBigIntegerField()),
                (
                    "assigned_object_type",
                    models.ForeignKey(
                        limit_choices_to=models.Q(
                            models.Q(("app_label", "ipam"), ("model", "ipaddress"))
                        ),
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="netbox_load_balancing.lbservice",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "verbose_name": "LB Service Assignment",
                "verbose_name_plural": "LB Service Assignments",
                "indexes": [
                    models.Index(
                        fields=["assigned_object_type", "assigned_object_id"],
                        name="netbox_load_assigne_87ff18_idx",
                    )
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=(
                            "assigned_object_type",
                            "assigned_object_id",
                            "service",
                        ),
                        name="netbox_load_balancing_lbserviceassignment_unique_service",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="MemberAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("assigned_object_id", models.PositiveBigIntegerField()),
                ("disabled", models.BooleanField(default=False)),
                (
                    "weight",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(32767),
                        ],
                    ),
                ),
                (
                    "assigned_object_type",
                    models.ForeignKey(
                        limit_choices_to=models.Q(
                            models.Q(
                                ("app_label", "netbox_load_balancing"),
                                ("model", "pool"),
                            ),
                            models.Q(
                                ("app_label", "netbox_load_balancing"),
                                ("model", "healthmonitor"),
                            ),
                        ),
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="netbox_load_balancing.member",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "verbose_name": "LB Member Assignment",
                "verbose_name_plural": "LB Member Assignments",
                "indexes": [
                    models.Index(
                        fields=["assigned_object_type", "assigned_object_id"],
                        name="netbox_load_assigne_b768a6_idx",
                    )
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("assigned_object_type", "assigned_object_id", "member"),
                        name="netbox_load_balancing_memberassignment_unique_member",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="PoolAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("assigned_object_id", models.PositiveBigIntegerField()),
                (
                    "assigned_object_type",
                    models.ForeignKey(
                        limit_choices_to=models.Q(
                            models.Q(("app_label", "ipam"), ("model", "iprange"))
                        ),
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "pool",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="netbox_load_balancing.pool",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "verbose_name": "LB Pool Assignment",
                "verbose_name_plural": "LB Pool Assignments",
                "indexes": [
                    models.Index(
                        fields=["assigned_object_type", "assigned_object_id"],
                        name="netbox_load_assigne_e7a970_idx",
                    )
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("assigned_object_type", "assigned_object_id", "pool"),
                        name="netbox_load_balancing_poolassignment_unique_pool",
                    )
                ],
            },
        ),
    ]
