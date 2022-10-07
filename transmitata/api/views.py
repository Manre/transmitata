from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_routes


class RoutesView(APIView):

    def get(self, request, route_name):
        response = get_routes(route_name=route_name)
        return Response(response)
