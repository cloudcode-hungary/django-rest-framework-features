from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_features import Feature


@Feature.view('this', 'that', get='getTest')
class TestView(APIView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return Response(200)
