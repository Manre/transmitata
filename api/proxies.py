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
        '200.116.226.210:57089',
        '186.97.238.11:4153',
        '181.143.21.146:4153',
        '201.184.239.74:5678',
        '186.97.236.242:5678',
        '181.129.51.147:47562',
        '181.205.36.210:5678',
        '181.48.193.42:2580',
        '201.184.75.210:4145',
        '181.78.16.237:5678',
        '181.129.138.114:32185',
        '190.182.88.242:30619',
        '191.102.82.83:4153',
        '181.49.212.122:5678',
        '181.118.158.38:4153',
        '190.131.198.77:7497',
        '190.253.241.254:5678',
        '45.229.192.61:5678',
        '200.106.216.64:63253',
        '200.106.216.50:63253',
        '191.102.107.234:999',
        '181.129.52.157:44665',
        '186.115.219.59:4153',
        '179.1.129.93:999',
        '190.109.2.89:4145',
        '181.143.199.106:5678',
        '190.182.88.214:30956',
        '190.145.182.4:4153',
        '181.205.46.178:4666',
        '181.78.8.43:5678',
        '201.184.230.34:5678',
        '186.97.233.58:5678',
        '181.129.62.2:47377',
        '201.184.243.77:8080',
    ]

    for raw_proxy in raw_proxy_list:
        url, port = raw_proxy.split(':')
        p = MyProxy(url=url, port=port)
        proxy_list.append(p)


init()
