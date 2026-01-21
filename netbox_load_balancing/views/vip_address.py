from netbox.views import generic
from utilities.views import register_model_view

from netbox_load_balancing.tables import VirtualIPTable
from netbox_load_balancing.filtersets import VirtualIPFilterSet

from netbox_load_balancing.models import VirtualIP
from netbox_load_balancing.forms import (
    VirtualIPFilterForm,
    VirtualIPForm,
    VirtualIPBulkEditForm,
    VirtualIPImportForm,
)

__all__ = (
    "VirtualIPView",
    "VirtualIPListView",
    "VirtualIPEditView",
    "VirtualIPDeleteView",
    "VirtualIPBulkEditView",
    "VirtualIPBulkDeleteView",
    "VirtualIPBulkImportView",
)


@register_model_view(VirtualIP)
class VirtualIPView(generic.ObjectView):
    queryset = VirtualIP.objects.all()
    template_name = "netbox_load_balancing/virtualip.html"


@register_model_view(VirtualIP, "list", path="", detail=False)
class VirtualIPListView(generic.ObjectListView):
    queryset = VirtualIP.objects.all()
    filterset = VirtualIPFilterSet
    filterset_form = VirtualIPFilterForm
    table = VirtualIPTable


@register_model_view(VirtualIP, "add", detail=False)
@register_model_view(VirtualIP, "edit")
class VirtualIPEditView(generic.ObjectEditView):
    queryset = VirtualIP.objects.all()
    form = VirtualIPForm


@register_model_view(VirtualIP, "delete")
class VirtualIPDeleteView(generic.ObjectDeleteView):
    queryset = VirtualIP.objects.all()


@register_model_view(VirtualIP, "bulk_edit", path="edit", detail=False)
class VirtualIPBulkEditView(generic.BulkEditView):
    queryset = VirtualIP.objects.all()
    filterset = VirtualIPFilterSet
    table = VirtualIPTable
    form = VirtualIPBulkEditForm


@register_model_view(VirtualIP, "bulk_delete", path="delete", detail=False)
class VirtualIPBulkDeleteView(generic.BulkDeleteView):
    queryset = VirtualIP.objects.all()
    table = VirtualIPTable


@register_model_view(VirtualIP, "bulk_import", detail=False)
class VirtualIPBulkImportView(generic.BulkImportView):
    queryset = VirtualIP.objects.all()
    model_form = VirtualIPImportForm
