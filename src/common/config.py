# -*- coding: utf-8 -*-

import os

import common.static as const


class ConfigHelper:
    @classmethod
    def get_redis_host(cls) -> str:
        return os.environ.get(const.REDIS_HOST_KEY, const.DEFAULT_REDIS_HOST)

    @classmethod
    def get_redis_port(cls) -> str:
        return os.environ.get(const.REDIS_PORT_KEY, const.DEFAULT_REDIS_PORT)

    @classmethod
    def get_mock_server_endpoint(cls) -> str:
        host = os.environ.get(const.MOKE_SERVER_HOST_KEY, const.DEFAULT_MOKE_SERVER_HOST)
        port = os.environ.get(const.MOKE_SERVER_PORT_KEY, const.DEFAULT_MOKE_SERVER_PORT)
        return f'{host}:{port}'
