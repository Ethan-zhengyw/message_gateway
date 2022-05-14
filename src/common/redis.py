# -*- coding: utf-8 -*-

import redis
from .config import ConfigHelper


class RedisHelper:
    def __init__(self, host, port):
        self.__pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
        self.__client = redis.Redis(connection_pool=self.__pool, decode_responses=True)

    @property
    def client(self):
        return self.__client


helper = RedisHelper(ConfigHelper.get_redis_host(), ConfigHelper.get_redis_port())
