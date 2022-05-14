# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class ILogger(metaclass=ABCMeta):
    @abstractmethod
    def info(self, msg: str):
        raise NotImplementedError

    @abstractmethod
    def warn(self, msg: str):
        raise NotImplementedError

    @abstractmethod
    def error(self, msg: str, exc: Exception = None):
        raise NotImplementedError

    @abstractmethod
    def fatal(self, msg: str, exc: Exception = None):
        raise NotImplementedError

    @abstractmethod
    def debug(self, msg: str):
        raise NotImplementedError
