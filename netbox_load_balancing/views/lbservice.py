from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view

from netbox_load_balancing.tables import LBServiceTable
from netbox_load_balancing.filtersets import LBServiceFilterSet

from netbox_load_balancing.models import LBService, LBServiceAssignment
from netbox_load_balancing.forms import (
    LBServiceFilterForm,
    LBServiceForm,
    LBServiceBulkEditForm,
    LBServiceAssignmentForm,
    LBServiceImportForm,
)

__all__ = (
    "LBServiceView",
    "LBServiceListView",
    "LBServiceEditView",
    "LBServiceDeleteView",
    "LBServiceBulkEditView",
    "LBServiceBulkDeleteView",
    "LBServiceBulkImportView",
    "LBServiceAssignmentEditView",
    "LBServiceAssignmentDeleteView",
)


@register_model_view(LBService)
class LBServiceView(generic.ObjectView):
    queryset = LBService.objects.all()
    template_name = "netbox_load_balancing/lbservice.html"


@register_model_view(LBService, "list", path="", detail=False)
class LBServiceListView(generic.ObjectListView):
    queryset = LBService.objects.all()
    filterset = LBServiceFilterSet
    filterset_form = LBServiceFilterForm
    table = LBServiceTable


@register_model_view(LBService, "add", detail=False)
@register_model_view(LBService, "edit")
class LBServiceEditView(generic.ObjectEditView):
    queryset = LBService.objects.all()
    form = LBServiceForm


@register_model_view(LBService, "delete")
class LBServiceDeleteView(generic.ObjectDeleteView):
    queryset = LBService.objects.all()


@register_model_view(LBService, "bulk_edit", path="edit", detail=False)
class LBServiceBulkEditView(generic.BulkEditView):
    queryset = LBService.objects.all()
    filterset = LBServiceFilterSet
    table = LBServiceTable
    form = LBServiceBulkEditForm


@register_model_view(LBService, "bulk_delete", path="delete", detail=False)
class LBServiceBulkDeleteView(generic.BulkDeleteView):
    queryset = LBService.objects.all()
    table = LBServiceTable


@register_model_view(LBService, "bulk_import", detail=False)
class LBServiceBulkImportView(generic.BulkImportView):
    queryset = LBService.objects.all()
    model_form = LBServiceImportForm


@register_model_view(LBServiceAssignment, "add", detail=False)
@register_model_view(LBServiceAssignment, "edit")
class LBServiceAssignmentEditView(generic.ObjectEditView):
    queryset = LBServiceAssignment.objects.all()
    form = LBServiceAssignmentForm

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


@register_model_view(LBServiceAssignment, "delete")
class LBServiceAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = LBServiceAssignment.objects.all()
