# -*- coding: utf-8 -*-

from typing import List
from abc import ABCMeta, abstractmethod


QueueMsgType = str


class IQueue(object, metaclass=ABCMeta):
    @abstractmethod
    def push(self, msg: QueueMsgType):
        raise NotImplementedError

    @abstractmethod
    def pop(self) -> QueueMsgType:
        """ pop element on top of the queue, return none if no element represent """
        raise NotImplementedError

    @abstractmethod
    def pop_or_block(self) -> List[QueueMsgType]:
        """ block until pop on element from queue """
        raise NotImplementedError
