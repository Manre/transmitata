import logging

import requests

logger = logging.getLogger(__name__)


def get_routes(route_name: str = "") -> list:
    if not route_name:
        logger.warning("No route name provided")
        return []

    headers = {
        "accept": "*/*",
        "appid": "9a2c3b48f0c24ae9bfba38e94f27c3ea",
        "user-agent": "MetroBus/1.9.7 (com.nexura.transmilenio; build:276; iOS 16.0.2) Alamofire/1.9.7",
        "accept-language": "en-US;q=1.0, es-US;q=0.9, es-419;q=0.8, ja-US;q=0.7",
    }

    url = 'http://tmsa-transmiapp-shvpc.uc.r.appspot.com/location/ruta?ruta={route_name}'

    logging_info = {
        "headers": headers,
        "url": url,
    }
    logger.warning(f"Getting routes with {logging_info}")

    try:
        response = requests.post(
            url.format(route_name=route_name),
            headers=headers,
            timeout=5,
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.ConnectTimeout:
        logger.error(f'Connection timeout when fetching routes for {route_name}')
        return []
    except requests.exceptions.ReadTimeout:
        logger.error(f'Read timeout when fetching routes for {route_name}')
        return []
    except requests.exceptions.ProxyError:
        logger.error(f'Proxy error when fetching routes for {route_name}')
        return []
    except requests.exceptions.ConnectionError:
        logger.error(f'Connection error when fetching routes for {route_name}')
        return []
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error {e.response.status_code} when fetching routes for {route_name}: {e}')
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f'Unexpected error when fetching routes for {route_name}: {e}')
        return []

    if response.text == '':
        logger.warning(f'Empty response when fetching routes for {route_name}')
        return []

    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f'JSON decode error when fetching routes for {route_name}: {e}')
        return []

    try:
        return [
            {
                "latitude": r['latitude'],
                "longitude": r['longitude'],
                "bus_id": r['label'],
                "route_name": route_name,
            }
            for r in json_response
        ]
    except KeyError as e:
        logger.error(f'Missing key {e} in route data for {route_name}')
        return []
    except TypeError:
        logger.error(f'Invalid data format in route response for {route_name}')
        return []


def find_route_by_name(route_name: str = "") -> list:
    if not route_name:
        logger.warning("No route name provided for search")
        return []

    url = (
        'https://api.buscador-rutas.transmilenio.gov.co/loader.php?lServicio=Rutas&lTipo=api&lFuncion=searchRutaByTipo&'
        f'tipo_ruta=TIPORUTA&search={route_name}'
    )

    headers = {
        'User-Agent': 'MetroBus/2.50 (com.nexura.transmilenio; build:345; iOS 26.1.0) Alamofire/4.9.1',
        'Host': 'api.buscador-rutas.transmilenio.gov.co',
    }

    try:
        response = requests.request("GET", url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectTimeout:
        logger.error(f'Connection timeout when searching for route {route_name}')
        return []
    except requests.exceptions.ReadTimeout:
        logger.error(f'Read timeout when searching for route {route_name}')
        return []
    except requests.exceptions.ConnectionError:
        logger.error(f'Connection error when searching for route {route_name}')
        return []
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error {e.response.status_code} when searching for route {route_name}: {e}')
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f'Unexpected error when searching for route {route_name}: {e}')
        return []

    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f'JSON decode error when searching for route {route_name}: {e}')
        return []

    try:
        routes_in_json = json_response.get("lista_rutas", [])
        
        return [
            {
                "route_id": route["id"],
                "route_code": route["codigo"],
                "route_name": route["nombre"],
            }
            for route in routes_in_json
        ]
    except KeyError as e:
        logger.error(f'Missing key {e} in route search results for {route_name}')
        return []
    except TypeError:
        logger.error(f'Invalid data format in route search response for {route_name}')
        return []


def find_stations_for_route(route_id: str = "") -> list:
    if not route_id:
        logger.warning("No route ID provided for station search")
        return []

    url = "https://api.buscador-rutas.transmilenio.gov.co/loader.php"
    params = {
        "lServicio": "Rutas",
        "lTipo": "api",
        "lFuncion": "infoRuta",
        "idRuta": route_id,
    }
    headers = {
        'User-Agent': (
            'MetroBus/2.50 (com.nexura.transmilenio; build:345; iOS 26.2.0) Alamofire/4.9.1'
        ),
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectTimeout:
        logger.error(f'Connection timeout when fetching stations for route {route_id}')
        return []
    except requests.exceptions.ReadTimeout:
        logger.error(f'Read timeout when fetching stations for route {route_id}')
        return []
    except requests.exceptions.ConnectionError:
        logger.error(f'Connection error when fetching stations for route {route_id}')
        return []
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error {e.response.status_code} when fetching stations for route {route_id}: {e}')
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f'Unexpected error when fetching stations for route {route_id}: {e}')
        return []

    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f'JSON decode error when fetching stations for route {route_id}: {e}')
        return []

    try:
        stations = [
            (
                lambda x: {
                    'lat': x[0],
                    'lon': x[1],
                }
            )(
                route_path['coordenada'].split(',')
            )
            for route_path in json_response['recorrido']['data']
        ]
        
        return stations
    except KeyError as e:
        logger.error(f'Missing key {e} in station data for route {route_id}')
        return []
    except TypeError:
        logger.error(f'Invalid data format in station response for route {route_id}')
        return []
    except Exception as e:
        logger.error(f'Unexpected error processing station data for route {route_id}: {e}')
        return []
