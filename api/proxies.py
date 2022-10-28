import logging
import random

logger = logging.getLogger(__name__)

proxy_list = []


class MyProxy:
    def __init__(self, url, port):
        self.url = url
        self.port = port
        self.response_count = 0

    def __str__(self):
        return self.response_count

    def get_proxy_url(self):
        return f"{self.url}:{self.port}"

    def add_response_count(self):
        self.response_count += 1

    def reduce_response_count(self):
        self.response_count -= 1


def find_proxy_by_response_count(response_count):
    for proxy in proxy_list:
        if proxy.response_count == response_count:
            return proxy
    raise Exception('¿?')


def get_proxies_with_best_responses(proxies: list):
    return [
        proxy
        for proxy in proxies
        if proxy >= 0
    ]


def get_proxy() -> MyProxy:
    current_proxies = [
        proxy.response_count
        for proxy in proxy_list
    ]

    current_proxies.sort(reverse=True)
    print(current_proxies)
    best_proxy_response = get_proxies_with_best_responses(proxies=current_proxies)
    if 0 < len(best_proxy_response) <= 3:
        response_count = random.choice(best_proxy_response)
    else:
        response_count = random.choice(current_proxies[:3])

    selected_proxy: MyProxy = find_proxy_by_response_count(response_count=response_count)

    logger.warning(f'Proxy found {selected_proxy.url} with response {str(selected_proxy.response_count)}')

    return selected_proxy


def init():
    """Proxies from http://free-proxy.cz/en/proxylist/country/CO/all/ping/all"""
    raw_proxy_list = [
        '190.61.88.147:8080',
        '191.102.107.234:999',
        '179.1.129.93:999',
        '201.184.243.77:8080',
        '190.61.35.165:8080',
        '190.90.224.198:999',
        '190.61.35.197:8080',
        '181.129.230.85:999',
        '190.109.18.65:8080',
        '190.61.41.106:999',
        '200.25.254.193:54240',
        '190.90.154.196:999',
        '190.109.6.113:999',
        '179.49.156.83:999',
        '200.106.167.114:999',
        '201.184.67.70:999',
        '138.117.84.65:999',
        '181.129.43.3:8080',
        '181.78.16.235:8080',
        '200.6.185.62:6969',
        '181.129.49.214:999',
        '181.78.16.225:999',
        '190.61.32.41:999',
        '181.78.15.105:999',
        '179.1.77.222:999',
        '201.182.251.154:8080',
        '200.106.184.13:999',
        '200.25.225.29:3128',
        '190.71.19.99:999',
        '181.205.106.106:9812',
        '190.85.141.170:9090',
        '186.179.99.6:999',
        '190.109.17.218:8080',
    ]

    for raw_proxy in raw_proxy_list:
        url, port = raw_proxy.split(':')
        p = MyProxy(url=url, port=port)
        proxy_list.append(p)


init()
