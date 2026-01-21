from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view

from netbox_load_balancing.tables import HealthMonitorTable
from netbox_load_balancing.filtersets import HealthMonitorFilterSet

from netbox_load_balancing.models import HealthMonitor, HealthMonitorAssignment
from netbox_load_balancing.forms import (
    HealthMonitorFilterForm,
    HealthMonitorForm,
    HealthMonitorBulkEditForm,
    HealthMonitorAssignmentForm,
    HealthMonitorImportForm,
)

__all__ = (
    "HealthMonitorView",
    "HealthMonitorListView",
    "HealthMonitorEditView",
    "HealthMonitorDeleteView",
    "HealthMonitorBulkEditView",
    "HealthMonitorBulkDeleteView",
    "HealthMonitorBulkImportView",
    "HealthMonitorAssignmentEditView",
    "HealthMonitorAssignmentDeleteView",
)


@register_model_view(HealthMonitor)
class HealthMonitorView(generic.ObjectView):
    queryset = HealthMonitor.objects.all()
    template_name = "netbox_load_balancing/healthmonitor.html"


@register_model_view(HealthMonitor, "list", path="", detail=False)
class HealthMonitorListView(generic.ObjectListView):
    queryset = HealthMonitor.objects.all()
    filterset = HealthMonitorFilterSet
    filterset_form = HealthMonitorFilterForm
    table = HealthMonitorTable


@register_model_view(HealthMonitor, "add", detail=False)
@register_model_view(HealthMonitor, "edit")
class HealthMonitorEditView(generic.ObjectEditView):
    queryset = HealthMonitor.objects.all()
    form = HealthMonitorForm


@register_model_view(HealthMonitor, "delete")
class HealthMonitorDeleteView(generic.ObjectDeleteView):
    queryset = HealthMonitor.objects.all()


@register_model_view(HealthMonitor, "bulk_edit", path="edit", detail=False)
class HealthMonitorBulkEditView(generic.BulkEditView):
    queryset = HealthMonitor.objects.all()
    filterset = HealthMonitorFilterSet
    table = HealthMonitorTable
    form = HealthMonitorBulkEditForm


@register_model_view(HealthMonitor, "bulk_delete", path="delete", detail=False)
class HealthMonitorBulkDeleteView(generic.BulkDeleteView):
    queryset = HealthMonitor.objects.all()
    table = HealthMonitorTable


@register_model_view(HealthMonitor, "bulk_import", detail=False)
class HealthMonitorBulkImportView(generic.BulkImportView):
    queryset = HealthMonitor.objects.all()
    model_form = HealthMonitorImportForm


@register_model_view(HealthMonitorAssignment, "add", detail=False)
@register_model_view(HealthMonitorAssignment, "edit")
class HealthMonitorAssignmentEditView(generic.ObjectEditView):
    queryset = HealthMonitorAssignment.objects.all()
    form = HealthMonitorAssignmentForm

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


@register_model_view(HealthMonitorAssignment, "delete")
class HealthMonitorAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = HealthMonitorAssignment.objects.all()
