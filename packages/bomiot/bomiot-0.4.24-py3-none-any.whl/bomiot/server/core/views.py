from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
import polars as pl
from rest_framework import viewsets, views

from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .serializers import FileRenderSerializer
from django.http import StreamingHttpResponse
from .files import CoreFile
from . import files as demo_app_file
from rest_framework.settings import api_settings

from .serializers import UserSerializer
from .filter import UserFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model


# def index(request):
#     """
#     render index page
#     :param request: request object
#     :return: page
#     """
#     return render(request, 'index.html')


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）

        list:
            Response a data list（all）

        create:
            Create a data line（post）

        delete:
            Delete a data line（delete)
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = UserFilter

    def get_project(self):
        try:
            id = self.kwargs.get('pk')
            return id
        except:
            return None

    def get_queryset(self):
        id = self.get_project()
        if self.request.user:
            if id is None:
                return User.objects.filter(openid=self.request.auth.openid, is_delete=False)
            else:
                return User.objects.filter(openid=self.request.auth.openid, id=id, is_delete=False)
        else:
            return User.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'create', 'destroy']:
            return UserSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        data['openid'] = self.request.auth.openid
        if ListModel.objects.filter(openid=data['openid'], bin_name=data['bin_name'], is_delete=False).exists():
            raise APIException({"detail": "Data exists"})
        else:
            if binsize.objects.filter(openid=data['openid'], bin_size=data['bin_size'], is_delete=False).exists():
                if binproperty.objects.filter(
                        Q(openid=data['openid'], bin_property=data['bin_property'], is_delete=False) |
                        Q(openid='init_data', bin_property=data['bin_property'], is_delete=False)).exists():
                    data['bar_code'] = Md5.md5(data['bin_name'])
                    serializer = self.get_serializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    scanner.objects.create(openid=self.request.auth.openid, mode="BINSET", code=data['bin_name'],
                                           bar_code=data['bar_code'])
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=200, headers=headers)
                else:
                    raise APIException({"detail": "Bin property does not exists or it has been changed"})
            else:
                raise APIException({"detail": "Bin size does not exists or it has been changed"})


    def destroy(self, request, pk):
        qs = self.get_object()
        if qs.openid != self.request.auth.openid:
            raise APIException({"detail": "Cannot delete data which not yours"})
        else:
            qs.is_delete = True
            qs.save()
            serializer = self.get_serializer(qs, many=False)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=200, headers=headers)