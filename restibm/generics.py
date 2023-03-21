import abc
from django.db import models
from rest_framework import generics
from rest_framework import viewsets
from restibm.utils import get_app_name
from restibm.utils import EXCEPT, INFO
from restibm.base import get_permission_instances
from restibm.base import get_filter_queryset
from restibm.base import API_FILTERS


class BaseAPIView(abc.ABC):
    public = False
    model = None
    queryset = None
    
    def __init__(self, *args, **kwargs):
        super(BaseAPIView, self).__init__(*args, **kwargs)
        if not issubclass(self.model, models.Model):
            raise TypeError(EXCEPT + (
                "The model class specified"
                " is not a subclass of django.db.models.Model."
                ))
        self.queryset = self.model.objects.all()
        # return self.model.objects.all()

    def get_permissions(self):
        """Permission instance recovery function.
        
        This function is called on each request received by the API.
        
        Returns:
            :obj:`list`: return the list of permission instances.
        """
        if not self.public:
            return get_permission_instances(self.request.method,
                                            api_view=self,
                                            model=self.model)
        else:
            return []


class BaseListAPIView(BaseAPIView, abc.ABC):
    filter_backends = API_FILTERS

    def list(self, request, *args, **kwargs):
        """The function that is executed to return a list of elements
        stored in the database"""
        if not self.public:
            app_name = get_app_name(self.__class__)
            self.queryset = get_filter_queryset(app_name)(model=self.model,
                                                          user=request.user)
        return super().list(request, *args, **kwargs)


class CreateAPIView(BaseAPIView, generics.CreateAPIView):
    pass


class ListAPIView(BaseListAPIView, generics.ListAPIView):
    pass


class RetrieveAPIView(BaseAPIView, generics.RetrieveAPIView):
    pass


class DestroyAPIView(BaseAPIView, generics.DestroyAPIView):
    pass


class ModelViewSet(BaseListAPIView, viewsets.ModelViewSet):
    pass
