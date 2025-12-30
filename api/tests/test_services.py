from unittest.mock import patch, Mock
import pytest
from api.services import get_routes, find_route_by_name, find_stations_for_route


class TestGetRoutes:
    """Test cases for get_routes function"""

    @patch('api.services.requests.post')
    def test_get_routes_success(self, mock_post):
        """Test successful retrieval of routes"""
        # Mock response data
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'latitude': 4.56,
                'longitude': -74.12,
                'label': 'T012'
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = get_routes('T1')

        # Assertions
        assert len(result) == 1
        assert result[0]['latitude'] == 4.56
        assert result[0]['longitude'] == -74.12
        assert result[0]['bus_id'] == 'T012'
        assert result[0]['route_name'] == 'T1'
        mock_post.assert_called_once()

    @patch('api.services.requests.post')
    def test_get_routes_empty_route_name(self, mock_post):
        """Test get_routes with empty route name"""
        result = get_routes('')
        assert result == []
        mock_post.assert_not_called()

    @patch('api.services.requests.post')
    def test_get_routes_connection_timeout(self, mock_post):
        """Test get_routes when connection times out"""
        from requests.exceptions import ConnectTimeout
        mock_post.side_effect = ConnectTimeout()

        result = get_routes('T1')
        assert result == []

    @patch('api.services.requests.post')
    def test_get_routes_empty_response(self, mock_post):
        """Test get_routes when empty response is returned"""
        mock_response = Mock()
        mock_response.text = ''
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = get_routes('T1')
        assert result == []

    @patch('api.services.requests.post')
    def test_get_routes_json_decode_error(self, mock_post):
        """Test get_routes when JSON decode error occurs"""
        from requests.exceptions import JSONDecodeError
        mock_response = Mock()
        mock_response.json.side_effect = JSONDecodeError('Invalid JSON', '', 0)
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = get_routes('T1')
        assert result == []


class TestFindRouteByName:
    """Test cases for find_route_by_name function"""

    @patch('api.services.requests.request')
    def test_find_route_by_name_success(self, mock_request):
        """Test successful route search"""
        # Mock response data
        mock_response = Mock()
        mock_response.json.return_value = {
            "lista_rutas": [
                {
                    "id": "123",
                    "codigo": "T1",
                    "nombre": "Transmilenio 1"
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        result = find_route_by_name('T1')

        # Assertions
        assert len(result) == 1
        assert result[0]['route_id'] == '123'
        assert result[0]['route_code'] == 'T1'
        assert result[0]['route_name'] == 'Transmilenio 1'
        mock_request.assert_called_once()

    @patch('api.services.requests.request')
    def test_find_route_by_name_empty_name(self, mock_request):
        """Test find_route_by_name with empty route name"""
        result = find_route_by_name('')
        assert result == []
        mock_request.assert_not_called()


class TestFindStationsForRoute:
    """Test cases for find_stations_for_route function"""

    @patch('api.services.requests.get')
    def test_find_stations_for_route_success(self, mock_get):
        """Test successful station retrieval"""
        # Mock response data
        mock_response = Mock()
        mock_response.json.return_value = {
            "recorrido": {
                "data": [
                    {
                        "coordenada": "4.56,-74.12"
                    }
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = find_stations_for_route('123')

        # Assertions
        assert len(result) == 1
        assert result[0]['lat'] == '4.56'
        assert result[0]['lon'] == '-74.12'
        mock_get.assert_called_once()

    @patch('api.services.requests.get')
    def test_find_stations_for_route_empty_id(self, mock_get):
        """Test find_stations_for_route with empty route ID"""
        result = find_stations_for_route('')
        assert result == []
        mock_get.assert_not_called()