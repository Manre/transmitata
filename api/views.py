from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import RouteCollection
from api.serializers import RouteCollectionDetailSerializer, RouteCollectionListSerializer
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


class RouteCollectionViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = RouteCollection.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return RouteCollectionListSerializer
        if self.action == 'retrieve':
            return RouteCollectionDetailSerializer
