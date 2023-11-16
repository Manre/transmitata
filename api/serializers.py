from rest_framework import serializers

from api.models import RouteCollection, Route


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['code', 'identification', 'description']


class RouteCollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteCollection
        fields = ['id', 'name']


class RouteCollectionDetailSerializer(serializers.ModelSerializer):
    routes = serializers.SerializerMethodField('get_routes')

    class Meta:
        model = RouteCollection
        fields = ['id', 'name', 'routes']
        ordering = ['routes']

    def get_routes(self, instance):
        routes = instance.routes.order_by('code')

        return RouteSerializer(routes, many=True, context=self.context).data
