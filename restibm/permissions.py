from rest_framework import permissions
from restibm.utils import get_app_name
from restibm.utils import INFO


class CorePermission(permissions.BasePermission):

    def __init__(self, api_view, model):
        super(CorePermission, self).__init__()
        self.app_name = get_app_name(api_view.__class__)

        if model is not None:
            model_name = model.__name__.lower()
            # self.model = model
            self.perms_map = {
                'GET': [f'{self.app_name}.view_{model_name}'],
                'OPTIONS': [f'{self.app_name}.view_{model_name}'],
                'HEAD': [f'{self.app_name}.view_{model_name}'],
                'POST': [f'{self.app_name}.add_{model_name}'],
                'PUT': [f'{self.app_name}.change_{model_name}'],
                'PATCH': [f'{self.app_name}.change_{model_name}'],
                'DELETE': [f'{self.app_name}.delete_{model_name}'],
            }

    def _get_perm_user(self, request):
        return request.user, self.perms_map[request.method][0]\
            if hasattr(self, 'perms_map')\
            else (None, None)

    def __str__(self):
        return "CorePermission"


class BaseAccessPermission(CorePermission):
    def has_permission(self, request, view):
        user, perm = self._get_perm_user(request)
        return user.has_perm(perm)


class BaseAccessObjectPermission(CorePermission):
    def has_object_permission(self, request, view, obj):
        user, perm = self._get_perm_user(request)
        return user.has_perm(perm) or user.has_perm(perm, obj)\
            if perm is not None\
            else False

