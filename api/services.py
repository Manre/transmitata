import logging
import random

import requests

logger = logging.getLogger(__name__)


def get_routes(route_name: str = None):
    headers = {
        "accept": "*/*",
        "appid": "9a2c3b48f0c24ae9bfba38e94f27c3ea",
        "user-agent": "MetroBus/1.9.7 (com.nexura.transmilenio; build:276; iOS 16.0.2) Alamofire/1.9.7",
        "accept-language": "en-US;q=1.0, es-US;q=0.9, es-419;q=0.8, ja-US;q=0.7",
    }
    proxy_list = [
        '190.61.88.147:8080',
        '45.7.132.102:8080',
        '181.129.49.214:999',
        '190.109.16.145:999',
        '181.225.101.14:999',
        '181.129.124.245:999',
        '200.25.254.193:54240',
        '190.61.48.25:999',
        '201.244.127.210:8080',
        '181.129.138.114:30838',
        '181.129.43.3:8080',
        '138.117.84.161:999',
        '181.78.27.34:999',
        '190.61.45.157:999',
        '181.78.16.235:8080',
        '181.205.41.210:7654',
        '200.106.187.242:999',
        '181.49.217.254:8080',
        '181.129.2.90:8081',
        '179.1.129.93:999',
    ]
    proxy = random.choice(proxy_list)
    logger.info(f'Using proxy: {proxy}')
    proxies = {'http': proxy}

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
            proxies=proxies,
        )
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        logger.error('Timeout error')
        return []

    if response.text == '':
        return []

    json_response = response.json()

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
    params = {
        "lServicio": "Rutas",
        "lTipo": "api",
        "lFuncion": "searchRutaByTipo",
        "tipo_ruta": "TIPORUTA",
        "search": route_name,
    }

    url = "https://www.transmilenio.gov.co/loader.php"
    response = requests.request("GET", url, params=params)

    json_response = response.json()

    routes_in_json = json_response.get("lista_rutas", [])

    return [
        {
            "route_code": route["codigo"],
            "route_name": route["nombre"],
        }
        for route in routes_in_json
    ]
