# -*- coding: utf-8 -*-

from typing import Callable
from abc import ABCMeta, abstractmethod


class IThreadManager(object, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def submit(cls, func: Callable, *args, raise_on_exception=False, **kwargs):
        raise NotImplementedError
