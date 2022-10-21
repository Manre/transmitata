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

    logger.warning(f'Proxy found {selected_proxy.url} with response {str(selected_proxy.response_count)}')

    return selected_proxy


def init():
    raw_proxy_list = [
        '190.61.88.147:8080',
        '190.14.229.242:5678',
        '181.48.153.30:8111',
        '186.97.144.98:5678',
        '186.97.172.178:5678',
        '186.87.179.54:5678',
        '201.184.230.34:5678',
        '190.131.198.77:7497',
        '143.137.99.202:5678',
        '152.204.128.46:35483',
        '201.184.239.74:5678',
        '181.129.62.2:47377',
        '181.129.74.186:5678',
        '181.49.23.78:999',
        '201.184.40.210:5678',
        '181.129.2.90:8081',
        '190.90.224.197:999',
        '45.7.132.102:8080',
        '190.109.168.217:8080',
        '200.106.187.246:999',
        '181.78.27.34:999',
        '181.48.70.30:4153',
        '201.184.75.210:4145',
        '200.118.122.6:4153',
        '201.220.85.22:5678',
        '190.144.167.178:5678',
        '190.60.28.31:80',
        '190.61.4.74:35721',
        '200.6.190.149:999',
        '200.116.226.210:43049',
        '200.25.254.157:8080',
        '190.121.153.93:999',
        '200.116.198.140:37092',
        '186.119.118.45:8082',
        '152.231.25.195:60080',
        '181.129.124.245:999',
    ]

    for raw_proxy in raw_proxy_list:
        url, port = raw_proxy.split(':')
        p = MyProxy(url=url, port=port)
        proxy_list.append(p)


init()
