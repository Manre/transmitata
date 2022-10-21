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


def get_proxy() -> MyProxy:
    current_proxies = [
        proxy.response_count
        for proxy in proxy_list
    ]

    current_proxies.sort(reverse=True)
    response_count = random.choice(current_proxies[:5])

    selected_proxy: MyProxy = find_proxy_by_response_count(response_count=response_count)

    logger.warning(f'Proxy found {selected_proxy.url}')

    return selected_proxy


def init():
    raw_proxy_list = [
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

    for raw_proxy in raw_proxy_list:
        url, port = raw_proxy.split(':')
        p = MyProxy(url=url, port=port)
        proxy_list.append(p)


init()
