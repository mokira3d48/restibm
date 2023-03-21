from rest_framework import viewsets
from restibm.generics import BaseListAPIView


class ModelViewSet(BaseListAPIView, viewsets.ModelViewSet):
    pass

