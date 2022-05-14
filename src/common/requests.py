# -*- coding: utf-8 -*-

import json
import requests

from .log import get_logger

__all__ = [
    "get",
    "post",
    "put",
    "Response"
]
logger = get_logger('common:request')
Response = requests.Response


def __request(method, url, **kwargs) -> requests.Response:
    print(f'{method} {url}: {json.dumps(kwargs)}')
    resp: requests.Response = requests.request(method, url, **kwargs)
    print(f'{method} {url} resp: ({resp.status_code} {resp.content})')
    return resp


def get(url, params=None, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return __request('get', url, params=params, **kwargs)


def post(url, data=None, json=None, **kwargs):
    return __request('post', url, data=data, json=json, **kwargs)


def put(url, data=None, **kwargs):
    return __request('put', url, data=data, **kwargs)
