# -*- coding: utf-8 -*-

from logging import getLogger

from lib.common.iface import ILogger


class MyLogger(ILogger):
    def __init__(self, name: str = None):
        self.__name = name
        self.__logger = getLogger(self.__name)

    def info(self, msg: str):
        msg = self.__add_prefix(msg)
        self.__logger.info(msg)

    def warn(self, msg: str):
        msg = self.__add_prefix(msg)
        self.__logger.warn(msg)

    def error(self, msg: str, exc: Exception = None):
        msg = self.__add_prefix(msg)
        self.__logger.error(msg, exc_info=exc)

    def fatal(self, msg: str, exc: Exception = None):
        msg = self.__add_prefix(msg)
        self.__logger.error(msg, exc_info=exc)

    def debug(self, msg: str):
        msg = self.__add_prefix(msg)
        self.__logger.debug(msg)

    def __add_prefix(self, msg: str) -> str:
        prefix = '{' + self.__name + '}'
        return f'{prefix}-{msg}'


def get_logger(name=None):
    return MyLogger(name)
