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
    routes = RouteSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = RouteCollection
        fields = ['id', 'name', 'routes']
