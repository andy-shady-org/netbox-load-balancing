from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view

from netbox_load_balancing.tables import VirtualIPPoolTable, VirtualIPTable
from netbox_load_balancing.filtersets import VirtualIPPoolFilterSet

from netbox_load_balancing.models import VirtualIPPool, VirtualIPPoolAssignment
from netbox_load_balancing.forms import (
    VirtualIPPoolFilterForm,
    VirtualIPPoolForm,
    VirtualIPPoolBulkEditForm,
    VirtualIPPoolAssignmentForm,
    VirtualIPPoolImportForm,
)


__all__ = (
    "VirtualIPPoolView",
    "VirtualIPPoolListView",
    "VirtualIPPoolEditView",
    "VirtualIPPoolDeleteView",
    "VirtualIPPoolBulkEditView",
    "VirtualIPPoolBulkDeleteView",
    "VirtualIPPoolBulkImportView",
    "VirtualIPPoolAssignmentEditView",
    "VirtualIPPoolAssignmentDeleteView",
)


@register_model_view(VirtualIPPool)
class VirtualIPPoolView(generic.ObjectView):
    queryset = VirtualIPPool.objects.all()
    template_name = "netbox_load_balancing/virtualippool.html"

    def get_extra_context(self, request, instance):
        virtual_ip_table = VirtualIPTable(
            instance.virtualip_related.all(), orderable=False, exclude=("virtual_pool",)
        )
        virtual_ip_table.configure(request)
        return {
            "virtual_ip_table": virtual_ip_table,
        }


@register_model_view(VirtualIPPool, "list", path="", detail=False)
class VirtualIPPoolListView(generic.ObjectListView):
    queryset = VirtualIPPool.objects.all()
    filterset = VirtualIPPoolFilterSet
    filterset_form = VirtualIPPoolFilterForm
    table = VirtualIPPoolTable


@register_model_view(VirtualIPPool, "add", detail=False)
@register_model_view(VirtualIPPool, "edit")
class VirtualIPPoolEditView(generic.ObjectEditView):
    queryset = VirtualIPPool.objects.all()
    form = VirtualIPPoolForm


@register_model_view(VirtualIPPool, "delete")
class VirtualIPPoolDeleteView(generic.ObjectDeleteView):
    queryset = VirtualIPPool.objects.all()


@register_model_view(VirtualIPPool, "bulk_edit", path="edit", detail=False)
class VirtualIPPoolBulkEditView(generic.BulkEditView):
    queryset = VirtualIPPool.objects.all()
    filterset = VirtualIPPoolFilterSet
    table = VirtualIPPoolTable
    form = VirtualIPPoolBulkEditForm


@register_model_view(VirtualIPPool, "bulk_delete", path="delete", detail=False)
class VirtualIPPoolBulkDeleteView(generic.BulkDeleteView):
    queryset = VirtualIPPool.objects.all()
    table = VirtualIPPoolTable


@register_model_view(VirtualIPPool, "bulk_import", detail=False)
class VirtualIPPoolBulkImportView(generic.BulkImportView):
    queryset = VirtualIPPool.objects.all()
    model_form = VirtualIPPoolImportForm


@register_model_view(VirtualIPPoolAssignment, "add", detail=False)
@register_model_view(VirtualIPPoolAssignment, "edit")
class VirtualIPPoolAssignmentEditView(generic.ObjectEditView):
    queryset = VirtualIPPoolAssignment.objects.all()
    form = VirtualIPPoolAssignmentForm

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


@register_model_view(VirtualIPPoolAssignment, "delete")
class VirtualIPPoolAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = VirtualIPPoolAssignment.objects.all()
