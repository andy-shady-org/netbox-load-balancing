from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view

from netbox_load_balancing.tables import PoolTable, ListenerTable
from netbox_load_balancing.filtersets import PoolFilterSet

from netbox_load_balancing.models import Pool, PoolAssignment
from netbox_load_balancing.forms import (
    PoolFilterForm,
    PoolForm,
    PoolBulkEditForm,
    PoolAssignmentForm,
    PoolImportForm,
)


__all__ = (
    "PoolView",
    "PoolListView",
    "PoolEditView",
    "PoolDeleteView",
    "PoolBulkEditView",
    "PoolBulkDeleteView",
    "PoolBulkImportView",
    "PoolAssignmentEditView",
    "PoolAssignmentDeleteView",
)


@register_model_view(Pool)
class PoolView(generic.ObjectView):
    queryset = Pool.objects.all()
    template_name = "netbox_load_balancing/pool.html"

    def get_extra_context(self, request, instance):
        listener_table = ListenerTable(instance.listeners.all(), orderable=False)
        listener_table.configure(request)
        return {
            "listener_table": listener_table,
        }


@register_model_view(Pool, "list", path="", detail=False)
class PoolListView(generic.ObjectListView):
    queryset = Pool.objects.all()
    filterset = PoolFilterSet
    filterset_form = PoolFilterForm
    table = PoolTable


@register_model_view(Pool, "add", detail=False)
@register_model_view(Pool, "edit")
class PoolEditView(generic.ObjectEditView):
    queryset = Pool.objects.all()
    form = PoolForm


@register_model_view(Pool, "delete")
class PoolDeleteView(generic.ObjectDeleteView):
    queryset = Pool.objects.all()


@register_model_view(Pool, "bulk_edit", path="edit", detail=False)
class PoolBulkEditView(generic.BulkEditView):
    queryset = Pool.objects.all()
    filterset = PoolFilterSet
    table = PoolTable
    form = PoolBulkEditForm


@register_model_view(Pool, "bulk_delete", path="delete", detail=False)
class PoolBulkDeleteView(generic.BulkDeleteView):
    queryset = Pool.objects.all()
    table = PoolTable


@register_model_view(Pool, "bulk_import", detail=False)
class PoolBulkImportView(generic.BulkImportView):
    queryset = Pool.objects.all()
    model_form = PoolImportForm


@register_model_view(PoolAssignment, "add", detail=False)
@register_model_view(PoolAssignment, "edit")
class PoolAssignmentEditView(generic.ObjectEditView):
    queryset = PoolAssignment.objects.all()
    form = PoolAssignmentForm

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


@register_model_view(PoolAssignment, "delete")
class PoolAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = PoolAssignment.objects.all()
