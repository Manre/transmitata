from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_routes, find_route_by_name


class RoutesView(APIView):

    def get(self, request, route_name):
        response = get_routes(route_name=route_name)
        return Response(response)


class FindRoutesView(APIView):

    def get(self, request, route_name):
        response = find_route_by_name(route_name=route_name)
        return Response(response)
