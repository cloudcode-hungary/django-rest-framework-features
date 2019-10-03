from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from . import schema


class CanAccessFeature(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_superuser:
            return True
        method = request.method.lower()
        meta = getattr(view, schema.REGISTRY_ATTR_NAME)
        try:
            description = meta[method][0]
        except KeyError:
            return False
        for codename in get_codenames_from_description(description):
            if request.user.has_perm(f'rest_framework_features.{codename}'):
                return True
        raise PermissionDenied(code=description[-1])


def get_codenames_from_description(description):
    return [
        '_'.join(description[:i])
        for i in range(1, len(description) + 1)
    ]


__all__ = (
    'CanAccessFeature',
    'get_codenames_from_description',
)
