import logging

import requests

logger = logging.getLogger(__name__)


def get_routes(route_name: str = None):
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
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ProxyError):
        logger.error('Timeout or proxy error')
        return []

    if response.text == '':
        return []

    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError:
        return []

    return [
        {
            "latitude": r['latitude'],
            "longitude": r['longitude'],
            "bus_id": r['label'],
            "route_name": route_name,
        }
        for r in json_response
    ]


def find_route_by_name(route_name: str = None) -> list:
    url = "https://www.transmilenio.gov.co/loader.php"
    params = {
        "lServicio": "Rutas",
        "lTipo": "api",
        "lFuncion": "searchRutaByTipo",
        "tipo_ruta": "TIPORUTA",
        "search": route_name,
    }
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
            'Version/18.4 Mobile/15E148 Safari/604.1'
        ),
    }

    response = requests.request("GET", url, params=params, headers=headers)

    json_response = response.json()

    routes_in_json = json_response.get("lista_rutas", [])

    return [
        {
            "route_id": route["id"],
            "route_code": route["codigo"],
            "route_name": route["nombre"],
        }
        for route in routes_in_json
    ]


def find_stations_for_route(route_id: str = None):
    url = "https://www.transmilenio.gov.co/loader.php"
    params = {
        "lServicio": "Rutas",
        "lTipo": "api",
        "lFuncion": "infoRuta",
        "idRuta": route_id,
    }
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
            'Version/18.4 Mobile/15E148 Safari/604.1'
        ),
    }

    response = requests.get(url, params=params, headers=headers)

    json_response = response.json()

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
