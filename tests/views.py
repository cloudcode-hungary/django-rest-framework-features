from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_features import schema


@schema.view('app', 'test', get=('read', 'listTests'))
class TestListView(ListAPIView):
    serializer_class = serializers.Serializer
    authentication_classes = (SessionAuthentication,)

    def get(self, request, *args, **kwargs):
        return Response(200)


@schema.view('app', 'test', get=('read', 'getTest'), delete=('write', 'deleteTest'))
class TestInstanceView(APIView):
    serializer_class = serializers.Serializer
    authentication_classes = (SessionAuthentication,)

    def get(self, request, *args, **kwargs):
        return Response(200)

    def delete(self, request, *args, **kwargs):
        return Response(200)


__all__ = (
    'TestListView',
    'TestInstanceView',
)
