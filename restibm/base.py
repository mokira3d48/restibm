import enum
import inspect
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import filters
from restibm.utils import INFO, ERRO, WARN
from restibm.permissions import BaseAccessPermission
from restibm.permissions import BaseAccessObjectPermission


# API rendering filter list.
API_FILTERS = [
    DjangoFilterBackend, 
    filters.SearchFilter,
    filters.OrderingFilter,
]


# Mapping between HTTP method and permission list.
PERMS_MAP = {
    'OPTIONS': [permissions.IsAuthenticated, BaseAccessPermission],
    'DELETE': [permissions.IsAuthenticated, BaseAccessObjectPermission],
    'PATCH': [permissions.IsAuthenticated, BaseAccessObjectPermission],
    'HEAD': [permissions.IsAuthenticated, BaseAccessPermission],
    'POST': [permissions.IsAuthenticated, BaseAccessPermission],
    'PUT': [permissions.IsAuthenticated, BaseAccessObjectPermission],
    'GET': [permissions.IsAuthenticated, BaseAccessObjectPermission],
}


class Authorization(enum.Enum):
    """Authorization value enum"""
    DELETE = 'delete'
    MODIFY = 'change'
    VIEW = 'view'


def get_permission_instances(http_method, *args, **kwargs):
    global PERMS_MAP
    perms_classes = PERMS_MAP[http_method]
    perm_objects = []
    for p in perms_classes:
        if inspect.isclass(p):
            if p != permissions.IsAuthenticated:
                perm_objects.append(p(*args, **kwargs))
            else:
                perm_objects.append(p())
        else:
            perm_objects.append(p)
    return perm_objects


def get_filter_queryset(app_name, option=None):
    """List filtering function based on permissions."""
    def f(model, user):
        # if model is not None and user is not None:
        queryset = model.objects.all()
        if None not in (model, user):
            mdn = model.__name__.lower()
            if not user.has_perm(f'{app_name}.view_{mdn}'):
                queryset = queryset.filter(Q(
                    pk__in=[o.pk
                            for o in queryset
                            if user.has_perm(f'{app_name}.view_{mdn}', o)]
                ))

        return queryset
    return f

