from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_routes, find_route_by_name, find_stations_for_route


class RoutesView(APIView):

    def get(self, request, route_name):
        response = get_routes(route_name=route_name)
        return Response(response)


class FindRoutesView(APIView):

    def get(self, request, route_name):
        response = find_route_by_name(route_name=route_name)
        return Response(response)


class FindStationsForRoute(APIView):

    def get(self, request, route_id):
        response = find_stations_for_route(route_id=route_id)
        return Response(response)
