from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Route, RouteCollection


class RoutesViewTest(APITestCase):
    """Test cases for RoutesView"""

    @patch('api.views.get_routes')
    def test_routes_view_success(self, mock_get_routes):
        """Test RoutesView with successful response"""
        mock_get_routes.return_value = [
            {'latitude': 4.56, 'longitude': -74.12, 'bus_id': 'T012', 'route_name': 'T1'}
        ]

        url = reverse('routes', kwargs={'route_name': 'T1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {'latitude': 4.56, 'longitude': -74.12, 'bus_id': 'T012', 'route_name': 'T1'}
        ])
        mock_get_routes.assert_called_once_with(route_name='T1')

    @patch('api.views.get_routes')
    def test_routes_view_empty_result(self, mock_get_routes):
        """Test RoutesView when service returns empty list"""
        mock_get_routes.return_value = []

        url = reverse('routes', kwargs={'route_name': 'INVALID'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        mock_get_routes.assert_called_once_with(route_name='INVALID')


class FindRoutesViewTest(APITestCase):
    """Test cases for FindRoutesView"""

    @patch('api.views.find_route_by_name')
    def test_find_routes_view_success(self, mock_find_route):
        """Test FindRoutesView with successful response"""
        mock_find_route.return_value = [
            {'route_id': '123', 'route_code': 'T1', 'route_name': 'Transmilenio 1'}
        ]

        url = reverse('find-routes', kwargs={'route_name': 'T1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {'route_id': '123', 'route_code': 'T1', 'route_name': 'Transmilenio 1'}
        ])
        mock_find_route.assert_called_once_with(route_name='T1')

    @patch('api.views.find_route_by_name')
    def test_find_routes_view_multiple_results(self, mock_find_route):
        """Test FindRoutesView with multiple routes returned"""
        mock_find_route.return_value = [
            {'route_id': '123', 'route_code': 'T1', 'route_name': 'Transmilenio 1'},
            {'route_id': '456', 'route_code': 'T2', 'route_name': 'Transmilenio 2'}
        ]

        url = reverse('find-routes', kwargs={'route_name': 'T'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        mock_find_route.assert_called_once_with(route_name='T')


class FindStationsForRouteViewTest(APITestCase):
    """Test cases for FindStationsForRoute view"""

    @patch('api.views.find_stations_for_route')
    def test_find_stations_view_success(self, mock_find_stations):
        """Test FindStationsForRoute with successful response"""
        mock_find_stations.return_value = [
            {'lat': '4.56', 'lon': '-74.12'},
            {'lat': '4.57', 'lon': '-74.13'}
        ]

        url = reverse('find-stations', kwargs={'route_id': '123'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {'lat': '4.56', 'lon': '-74.12'},
            {'lat': '4.57', 'lon': '-74.13'}
        ])
        mock_find_stations.assert_called_once_with(route_id='123')


class RouteCollectionViewSetTest(APITestCase):
    """Test cases for RouteCollectionViewSet"""

    def setUp(self):
        """Set up test data"""
        self.route1 = Route.objects.create(
            code="T1",
            identification=123,
            description="Transmilenio Line 1"
        )
        self.route2 = Route.objects.create(
            code="T2",
            identification=456,
            description="Transmilenio Line 2"
        )
        self.route_collection = RouteCollection.objects.create(
            name="Main Routes"
        )
        self.route_collection.routes.add(self.route1, self.route2)

    def test_list_route_collections(self):
        """Test listing route collections"""
        url = reverse('routecollection-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Main Routes')

    def test_retrieve_route_collection_detail(self):
        """Test retrieving a specific route collection with detail"""
        url = reverse('routecollection-detail', kwargs={'id': self.route_collection.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Main Routes')
        self.assertEqual(len(response.data['routes']), 2)

    def test_retrieve_route_collection_not_found(self):
        """Test retrieving a non-existent route collection"""
        url = reverse('routecollection-detail', kwargs={'id': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)