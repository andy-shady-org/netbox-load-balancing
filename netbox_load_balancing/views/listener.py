from netbox.views import generic
from utilities.views import register_model_view

from netbox_load_balancing.tables import ListenerTable
from netbox_load_balancing.filtersets import ListenerFilterSet

from netbox_load_balancing.models import Listener
from netbox_load_balancing.forms import (
    ListenerFilterForm,
    ListenerForm,
    ListenerBulkEditForm,
    ListenerImportForm,
)

__all__ = (
    "ListenerView",
    "ListenerListView",
    "ListenerEditView",
    "ListenerDeleteView",
    "ListenerBulkEditView",
    "ListenerBulkDeleteView",
    "ListenerBulkImportView",
)


@register_model_view(Listener)
class ListenerView(generic.ObjectView):
    queryset = Listener.objects.all()
    template_name = "netbox_load_balancing/listener.html"


@register_model_view(Listener, "list", path="", detail=False)
class ListenerListView(generic.ObjectListView):
    queryset = Listener.objects.all()
    filterset = ListenerFilterSet
    filterset_form = ListenerFilterForm
    table = ListenerTable


@register_model_view(Listener, "add", detail=False)
@register_model_view(Listener, "edit")
class ListenerEditView(generic.ObjectEditView):
    queryset = Listener.objects.all()
    form = ListenerForm


@register_model_view(Listener, "delete")
class ListenerDeleteView(generic.ObjectDeleteView):
    queryset = Listener.objects.all()


@register_model_view(Listener, "bulk_edit", path="edit", detail=False)
class ListenerBulkEditView(generic.BulkEditView):
    queryset = Listener.objects.all()
    filterset = ListenerFilterSet
    table = ListenerTable
    form = ListenerBulkEditForm


@register_model_view(Listener, "bulk_delete", path="delete", detail=False)
class ListenerBulkDeleteView(generic.BulkDeleteView):
    queryset = Listener.objects.all()
    table = ListenerTable


@register_model_view(Listener, "bulk_import", detail=False)
class ListenerBulkImportView(generic.BulkImportView):
    queryset = Listener.objects.all()
    model_form = ListenerImportForm
