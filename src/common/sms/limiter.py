# -*- coding: utf-8 -*-

from dramatiq.errors import RateLimitExceeded
from dramatiq.rate_limits import WindowRateLimiter
from dramatiq.rate_limits.backends import RedisBackend
from werkzeug.exceptions import InternalServerError

import common.static as const
from common.redis import helper as redis_helper
from .types import *

backend = RedisBackend(client=redis_helper.client)


def typed_rate_limit_wrapper(api_or_tel: LIMIT_TYPE):
    def rate_limit_wrapper(func):
        def wrapped(cls, msg: SendReq):

            def __decode_limit_params() -> (str, int, int):
                if api_or_tel == LIMIT_TYPE_API:
                    return f'{const.APP_NAME}_limit_{LIMIT_TYPE_API}', API_LIMIT, LIMIT_WINDOW

                elif api_or_tel == LIMIT_TYPE_TEL:
                    return f'{const.APP_NAME}_limit_{LIMIT_TYPE_TEL}_{msg.acceptor_tel}', TEL_LIMIT, LIMIT_WINDOW

                else:
                    raise InternalServerError(f'unexpected limit type: {api_or_tel}')

            limit_key, limit_value, limit_window = __decode_limit_params()

            try:
                with WindowRateLimiter(
                        backend, limit_key, limit=limit_value, window=limit_window).acquire():
                    return func(cls, msg)

            except RateLimitExceeded as e:
                raise e

        return wrapped

    return rate_limit_wrapper
