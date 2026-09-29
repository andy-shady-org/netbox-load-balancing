from django.contrib.postgres.aggregates import JSONBAgg
from django.db.models import Q
from extras.models import ConfigContextModel
from utilities.data import deepmerge

__all__ = (
    "get_config_contexts_for_lb_service",
    "LBServiceConfigContextViewMixin",
    "LBServiceConfigContextView",
    "LBServiceConfigContextModelMixin",
)


def get_config_contexts_for_lb_service(user, instance, aggregate_data=False):
    """
    Utility function to get ConfigContexts for an LBService with permission filtering.

    Since we cannot modify the NetBox ConfigContext model, this function wraps
    the custom queryset logic and applies it to the standard ConfigContext.objects queryset.

    Args:
        user: The requesting user (for permission filtering). If None, skips permission checks.
        instance: The LBService instance
        aggregate_data: If True, return aggregated JSON data instead of QuerySet

    Returns:
        QuerySet of ConfigContext objects, or aggregated JSON data if aggregate_data=True
    """
    from extras.models import ConfigContext

    tenant_group = instance.tenant.group if instance.tenant else None

    queryset = (
        ConfigContext.objects.filter(
            Q(tenant_groups=tenant_group) | Q(tenant_groups=None),
            Q(tenants=instance.tenant) | Q(tenants=None),
            Q(tags__slug__in=instance.tags.slugs()) | Q(tags=None),
            is_active=True,
        )
        .order_by("weight", "name")
        .distinct()
    )

    # Only apply permission filtering if user is provided
    if user is not None:
        queryset = queryset.restrict(user, "view")

    if aggregate_data:
        return queryset.aggregate(
            config_context_data=JSONBAgg("data", order_by=["weight", "name"])
        )["config_context_data"]

    return queryset


class LBServiceConfigContextViewMixin:
    """
    Mixin for views that display config context for LBService-compatible models.

    This provides the get_extra_context() method that should be combined with
    ObjectConfigContextView in your view subclass.
    """

    base_template = "generic/object.html"

    def get_extra_context(self, request, instance):
        source_contexts = get_config_contexts_for_lb_service(request.user, instance)

        # Determine user's preferred output format
        if request.GET.get("format") in ["json", "yaml"]:
            format = request.GET.get("format")
            if request.user.is_authenticated:
                request.user.config.set("data_format", format, commit=True)
        elif request.user.is_authenticated:
            format = request.user.config.get("data_format", "json")
        else:
            format = "json"

        return {
            "rendered_context": instance.get_config_context(),
            "source_contexts": source_contexts,
            "format": format,
            "base_template": self.base_template,
        }


# For backwards compatibility, create an alias
LBServiceConfigContextView = LBServiceConfigContextViewMixin


class LBServiceConfigContextModelMixin(ConfigContextModel):
    """
    Mixin for models that need LBService-style ConfigContext rendering.

    Inherits from ConfigContextModel to provide:
    - _config_context_data (cache field)
    - _config_context_generation (cache counter)
    - local_context_data (local overrides)
    - get_config_context() method

    Overrides render_config_context() to use tenant/tenant_group/tags
    instead of the standard Device/VM logic.
    """

    def render_config_context(self):
        """
        Compile config context data for models using tenant, tenant_group, and tags.

        Uses user=None to skip permission filtering (permissions are checked at view/API level).
        Model-level rendering should return all applicable contexts.
        """
        data = {}

        # Get ConfigContexts applicable to models (tenant, tenant_group, tags only)
        # Pass user=None to skip permission filtering (permissions happen at view/API level)
        # Model-level rendering must return ALL applicable contexts, not just user-visible ones
        config_context_data = (
            get_config_contexts_for_lb_service(None, self, aggregate_data=True) or []
        )

        for context in config_context_data:
            data = deepmerge(data, context)

        # If the object has local config context data defined, merge it last
        if self.local_context_data:
            data = deepmerge(data, self.local_context_data)

        return data

    class Meta:
        abstract = True
