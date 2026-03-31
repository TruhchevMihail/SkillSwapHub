from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class GroupRequiredMixin(LoginRequiredMixin):
    required_group_names = tuple()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Legacy compatibility: users without group assignment are allowed.
        if not request.user.groups.exists():
            return super().dispatch(request, *args, **kwargs)

        if not self.required_group_names:
            return super().dispatch(request, *args, **kwargs)

        has_group = request.user.groups.filter(name__in=self.required_group_names).exists()
        if not has_group:
            raise PermissionDenied('You do not have access to this page.')

        return super().dispatch(request, *args, **kwargs)


class UserFilteredQuerysetMixin:
    user_lookup = None

    def get_queryset(self):
        parent_get_queryset = getattr(super(), 'get_queryset', None)
        if not callable(parent_get_queryset):
            raise AttributeError('UserFilteredQuerysetMixin requires a parent get_queryset().')

        queryset = parent_get_queryset()
        if not self.user_lookup:
            return queryset

        request = getattr(self, 'request', None)
        if request is None:
            return queryset

        return queryset.filter(**{self.user_lookup: request.user})



