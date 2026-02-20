from unittest.mock import Mock, patch

import pytest

from api.exceptions import TransmilenioAPIError
from api.services import find_route_by_name, find_stations_for_route, get_routes


class TestGetRoutes:
    """Test cases for get_routes function"""

    @patch('api.services.requests.post')
    def test_get_routes_success(self, mock_post):
        """Test successful retrieval of routes"""
        # Mock response data
        mock_response = Mock()
        mock_response.json.return_value = [{'latitude': 4.56, 'longitude': -74.12, 'label': 'T012'}]
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
        """Test get_routes when connection times out raises TransmilenioAPIError"""
        from requests.exceptions import ConnectTimeout

        mock_post.side_effect = ConnectTimeout()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            get_routes('T1')
        assert 'Tiempo de espera agotado al conectar con Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.post')
    def test_get_routes_read_timeout(self, mock_post):
        """Test get_routes when read times out raises TransmilenioAPIError"""
        from requests.exceptions import ReadTimeout

        mock_post.side_effect = ReadTimeout()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            get_routes('T1')
        assert 'Transmilenio tardó demasiado en responder' in str(exc_info.value)

    @patch('api.services.requests.post')
    def test_get_routes_connection_error(self, mock_post):
        """Test get_routes when connection fails raises TransmilenioAPIError"""
        from requests.exceptions import ConnectionError

        mock_post.side_effect = ConnectionError()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            get_routes('T1')
        assert 'No se pudo conectar con Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.post')
    def test_get_routes_proxy_error(self, mock_post):
        """Test get_routes when proxy fails raises TransmilenioAPIError"""
        from requests.exceptions import ProxyError

        mock_post.side_effect = ProxyError()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            get_routes('T1')
        assert 'Error de conexión con Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.post')
    def test_get_routes_http_error(self, mock_post):
        """Test get_routes when HTTP error occurs raises TransmilenioAPIError"""
        from requests.exceptions import HTTPError

        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.side_effect = HTTPError(response=mock_response)

        with pytest.raises(TransmilenioAPIError) as exc_info:
            get_routes('T1')
        assert 'Transmilenio respondió con error (500)' in str(exc_info.value)

    @patch('api.services.requests.post')
    def test_get_routes_request_exception(self, mock_post):
        """Test get_routes when unexpected request error occurs raises TransmilenioAPIError"""
        from requests.exceptions import RequestException

        mock_post.side_effect = RequestException()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            get_routes('T1')
        assert 'Error inesperado al consultar Transmilenio' in str(exc_info.value)

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
        """Test get_routes when JSON decode error occurs raises TransmilenioAPIError"""
        from requests.exceptions import JSONDecodeError

        mock_response = Mock()
        mock_response.text = 'invalid'
        mock_response.json.side_effect = JSONDecodeError('Invalid JSON', '', 0)
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        with pytest.raises(TransmilenioAPIError) as exc_info:
            get_routes('T1')
        assert 'Respuesta inválida de Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.post')
    def test_get_routes_missing_key_error(self, mock_post):
        """Test get_routes when response is missing required keys raises TransmilenioAPIError"""
        mock_response = Mock()
        mock_response.text = '[{"latitude": 4.56}]'
        mock_response.json.return_value = [{'latitude': 4.56}]  # Missing longitude and label
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        with pytest.raises(TransmilenioAPIError) as exc_info:
            get_routes('T1')
        assert 'Datos incompletos en la respuesta de Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.post')
    def test_get_routes_invalid_data_format(self, mock_post):
        """Test get_routes when response has invalid data format raises TransmilenioAPIError"""
        mock_response = Mock()
        mock_response.text = 'null'
        mock_response.json.return_value = None  # Not iterable
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        with pytest.raises(TransmilenioAPIError) as exc_info:
            get_routes('T1')
        assert 'Formato de datos inesperado de Transmilenio' in str(exc_info.value)


class TestFindRouteByName:
    """Test cases for find_route_by_name function"""

    @patch('api.services.requests.request')
    def test_find_route_by_name_success(self, mock_request):
        """Test successful route search"""
        # Mock response data
        mock_response = Mock()
        mock_response.json.return_value = {'lista_rutas': [{'id': '123', 'codigo': 'T1', 'nombre': 'Transmilenio 1'}]}
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

    @patch('api.services.requests.request')
    def test_find_route_by_name_connection_timeout(self, mock_request):
        """Test find_route_by_name when connection times out raises TransmilenioAPIError"""
        from requests.exceptions import ConnectTimeout

        mock_request.side_effect = ConnectTimeout()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_route_by_name('T1')
        assert 'Tiempo de espera agotado al conectar con Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.request')
    def test_find_route_by_name_read_timeout(self, mock_request):
        """Test find_route_by_name when read times out raises TransmilenioAPIError"""
        from requests.exceptions import ReadTimeout

        mock_request.side_effect = ReadTimeout()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_route_by_name('T1')
        assert 'Transmilenio tardó demasiado en responder' in str(exc_info.value)

    @patch('api.services.requests.request')
    def test_find_route_by_name_connection_error(self, mock_request):
        """Test find_route_by_name when connection fails raises TransmilenioAPIError"""
        from requests.exceptions import ConnectionError

        mock_request.side_effect = ConnectionError()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_route_by_name('T1')
        assert 'No se pudo conectar con Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.request')
    def test_find_route_by_name_http_error(self, mock_request):
        """Test find_route_by_name when HTTP error occurs raises TransmilenioAPIError"""
        from requests.exceptions import HTTPError

        mock_response = Mock()
        mock_response.status_code = 503
        mock_request.side_effect = HTTPError(response=mock_response)

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_route_by_name('T1')
        assert 'Transmilenio respondió con error (503)' in str(exc_info.value)

    @patch('api.services.requests.request')
    def test_find_route_by_name_json_decode_error(self, mock_request):
        """Test find_route_by_name when JSON decode error occurs raises TransmilenioAPIError"""
        from requests.exceptions import JSONDecodeError

        mock_response = Mock()
        mock_response.json.side_effect = JSONDecodeError('Invalid JSON', '', 0)
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_route_by_name('T1')
        assert 'Respuesta inválida de Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.request')
    def test_find_route_by_name_missing_key_error(self, mock_request):
        """Test find_route_by_name when response is missing required keys raises TransmilenioAPIError"""
        mock_response = Mock()
        mock_response.json.return_value = {'lista_rutas': [{'id': '123'}]}  # Missing codigo and nombre
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_route_by_name('T1')
        assert 'Datos incompletos en la respuesta de Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.request')
    def test_find_route_by_name_invalid_data_format(self, mock_request):
        """Test find_route_by_name when response has invalid data format raises TransmilenioAPIError"""
        mock_response = Mock()
        mock_response.json.return_value = {'lista_rutas': 'not_a_list'}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_route_by_name('T1')
        assert 'Formato de datos inesperado de Transmilenio' in str(exc_info.value)


class TestFindStationsForRoute:
    """Test cases for find_stations_for_route function"""

    @patch('api.services.requests.get')
    def test_find_stations_for_route_success(self, mock_get):
        """Test successful station retrieval"""
        # Mock response data
        mock_response = Mock()
        mock_response.json.return_value = {'recorrido': {'data': [{'coordenada': '4.56,-74.12'}]}}
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

    @patch('api.services.requests.get')
    def test_find_stations_for_route_connection_timeout(self, mock_get):
        """Test find_stations_for_route when connection times out raises TransmilenioAPIError"""
        from requests.exceptions import ConnectTimeout

        mock_get.side_effect = ConnectTimeout()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_stations_for_route('123')
        assert 'Tiempo de espera agotado al conectar con Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.get')
    def test_find_stations_for_route_read_timeout(self, mock_get):
        """Test find_stations_for_route when read times out raises TransmilenioAPIError"""
        from requests.exceptions import ReadTimeout

        mock_get.side_effect = ReadTimeout()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_stations_for_route('123')
        assert 'Transmilenio tardó demasiado en responder' in str(exc_info.value)

    @patch('api.services.requests.get')
    def test_find_stations_for_route_connection_error(self, mock_get):
        """Test find_stations_for_route when connection fails raises TransmilenioAPIError"""
        from requests.exceptions import ConnectionError

        mock_get.side_effect = ConnectionError()

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_stations_for_route('123')
        assert 'No se pudo conectar con Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.get')
    def test_find_stations_for_route_http_error(self, mock_get):
        """Test find_stations_for_route when HTTP error occurs raises TransmilenioAPIError"""
        from requests.exceptions import HTTPError

        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.side_effect = HTTPError(response=mock_response)

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_stations_for_route('123')
        assert 'Transmilenio respondió con error (404)' in str(exc_info.value)

    @patch('api.services.requests.get')
    def test_find_stations_for_route_json_decode_error(self, mock_get):
        """Test find_stations_for_route when JSON decode error occurs raises TransmilenioAPIError"""
        from requests.exceptions import JSONDecodeError

        mock_response = Mock()
        mock_response.json.side_effect = JSONDecodeError('Invalid JSON', '', 0)
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_stations_for_route('123')
        assert 'Respuesta inválida de Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.get')
    def test_find_stations_for_route_missing_key_error(self, mock_get):
        """Test find_stations_for_route when response is missing required keys raises TransmilenioAPIError"""
        mock_response = Mock()
        mock_response.json.return_value = {'recorrido': {}}  # Missing 'data' key
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_stations_for_route('123')
        assert 'Datos incompletos en la respuesta de Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.get')
    def test_find_stations_for_route_invalid_data_format(self, mock_get):
        """Test find_stations_for_route when response has invalid data format raises TransmilenioAPIError"""
        mock_response = Mock()
        mock_response.json.return_value = {'recorrido': {'data': 'not_a_list'}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_stations_for_route('123')
        assert 'Formato de datos inesperado de Transmilenio' in str(exc_info.value)

    @patch('api.services.requests.get')
    def test_find_stations_for_route_invalid_coordenada_format(self, mock_get):
        """Test find_stations_for_route when coordenada has invalid format raises TransmilenioAPIError"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'recorrido': {
                'data': [{'coordenada': 'invalid'}]  # Missing comma separator
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(TransmilenioAPIError) as exc_info:
            find_stations_for_route('123')
        assert 'Error inesperado al procesar datos de estaciones' in str(exc_info.value)
