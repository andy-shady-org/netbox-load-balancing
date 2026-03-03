from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view

from netbox_load_balancing.tables import (
    MemberTable,
    PoolTable,
    HealthMonitorTable,
)
from netbox_load_balancing.filtersets import MemberFilterSet

from netbox_load_balancing.models import Member, MemberAssignment, Pool, HealthMonitor
from netbox_load_balancing.forms import (
    MemberFilterForm,
    MemberForm,
    MemberBulkEditForm,
    MemberAssignmentForm,
    MemberImportForm,
)

__all__ = (
    "MemberView",
    "MemberListView",
    "MemberEditView",
    "MemberDeleteView",
    "MemberBulkEditView",
    "MemberBulkDeleteView",
    "MemberBulkImportView",
    "MemberAssignmentEditView",
    "MemberAssignmentDeleteView",
)


@register_model_view(Member)
class MemberView(generic.ObjectView):
    queryset = Member.objects.all()
    template_name = "netbox_load_balancing/member.html"

    def get_extra_context(self, request, instance):
        pool_assignments_table = PoolTable(
            Pool.objects.filter(members__member=instance),
            orderable=False,
        )
        pool_assignments_table.configure(request)
        monitor_assignments_table = HealthMonitorTable(
            HealthMonitor.objects.filter(members__member=instance),
            orderable=False,
        )
        monitor_assignments_table.configure(request)
        return {
            "pool_assignment_table": pool_assignments_table,
            "monitor_assignments_table": monitor_assignments_table,
        }


@register_model_view(Member, "list", path="", detail=False)
class MemberListView(generic.ObjectListView):
    queryset = Member.objects.all()
    filterset = MemberFilterSet
    filterset_form = MemberFilterForm
    table = MemberTable


@register_model_view(Member, "add", detail=False)
@register_model_view(Member, "edit")
class MemberEditView(generic.ObjectEditView):
    queryset = Member.objects.all()
    form = MemberForm


@register_model_view(Member, "delete")
class MemberDeleteView(generic.ObjectDeleteView):
    queryset = Member.objects.all()


@register_model_view(Member, "bulk_edit", path="edit", detail=False)
class MemberBulkEditView(generic.BulkEditView):
    queryset = Member.objects.all()
    filterset = MemberFilterSet
    table = MemberTable
    form = MemberBulkEditForm


@register_model_view(Member, "bulk_delete", path="delete", detail=False)
class MemberBulkDeleteView(generic.BulkDeleteView):
    queryset = Member.objects.all()
    table = MemberTable


@register_model_view(Member, "bulk_import", detail=False)
class MemberBulkImportView(generic.BulkImportView):
    queryset = Member.objects.all()
    model_form = MemberImportForm


@register_model_view(MemberAssignment, "add", detail=False)
@register_model_view(MemberAssignment, "edit")
class MemberAssignmentEditView(generic.ObjectEditView):
    queryset = MemberAssignment.objects.all()
    form = MemberAssignmentForm

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk:
            content_type = get_object_or_404(
                ContentType, pk=request.GET.get("assigned_object_type")
            )
            instance.assigned_object = get_object_or_404(
                content_type.model_class(), pk=request.GET.get("assigned_object_id")
            )
        return instance

    def get_extra_addanother_params(self, request):
        return {
            "assigned_object_type": request.GET.get("assigned_object_type"),
            "assigned_object_id": request.GET.get("assigned_object_id"),
        }


@register_model_view(MemberAssignment, "delete")
class MemberAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = MemberAssignment.objects.all()
