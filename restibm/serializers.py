import abc
from rest_framework import serializers
from guardian.shortcuts import assign_perm
from restibm.utils import get_app_name


class ModelSerializer(serializers.ModelSerializer):
    authorizations = '__all__'

    class Meta:
        model = None

    def save(self, **kwargs):
        x = super().save(**kwargs)
        if self.Meta.model is not None:
            # definition of permission to this owner
            mname = self.Meta.model.__name__.lower()
            user = self.context['request'].user\
                if not hasattr(self, 'owner')\
                else self.owner
            app_name = get_app_name(self.__class__)
            if user.is_authenticated:
                if self.authorizations == '__all__':
                    assign_perm(f'{app_name}.view_{mname}', user, x)
                    assign_perm(f'{app_name}.add_{mname}', user, x)
                    assign_perm(f'{app_name}.change_{mname}', user, x)
                    assign_perm(f'{app_name}.delete_{mname}', user, x)
                else:
                    if type(self.authorizations) is list:
                        for auth in self.authorizations:
                            perm_string = (
                                f'{app_name}'
                                f'.{auth.value}_{mname}'
                                )
                            assign_perm(perm_string, user, x)
        return x

