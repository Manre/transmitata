import requests


def get_routes(route_name: str = None):
    headers = {
        "accept": "*/*",
        "appid": "9a2c3b48f0c24ae9bfba38e94f27c3ea",
        "user-agent": "MetroBus/1.9.7 (com.nexura.transmilenio; build:276; iOS 16.0.2) Alamofire/1.9.7",
        "accept-language": "en-US;q=1.0, es-US;q=0.9, es-419;q=0.8, ja-US;q=0.7",
    }

    url = 'https://tmsa-transmiapp-shvpc.uc.r.appspot.com/location/ruta?ruta={route_name}'

    response = requests.post(
        url.format(route_name=route_name),
        headers=headers,
    )

    json_response = response.json()

    return [
        {
            "latitude": r['latitude'],
            "longitude": r['longitude'],
            "title": route_name
        }
        for r in json_response
    ]
