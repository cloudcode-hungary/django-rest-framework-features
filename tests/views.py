from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_features import schema


@schema.view('app', 'test', 'read', get='listTests')
class TestListView(APIView):
    authentication_classes = (SessionAuthentication,)

    def get(self, request, *args, **kwargs):
        return Response(200)


@schema.view('app', 'test', 'read', get='getTest')
class TestRetrieveView(APIView):
    authentication_classes = (SessionAuthentication,)

    def get(self, request, *args, **kwargs):
        return Response(200)


@schema.view('app', 'test', 'write', delete='deleteTest')
class TestDestroyView(APIView):
    authentication_classes = (SessionAuthentication,)

    def delete(self, request, *args, **kwargs):
        return Response(200)


__all__ = (
    'TestListView',
    'TestRetrieveView',
    'TestDestroyView',
)
