from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_features import Feature


@Feature.view('app', 'test', get='listTests')
class TestListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(200)


@Feature.view('app', 'test', get='getTest', delete='deleteTest')
class TestRetrieveDestroyView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(200)

    def delete(self, request, *args, **kwargs):
        return Response(200)


__all__ = (
    'TestListView',
    'TestRetrieveDestroyView',
)
