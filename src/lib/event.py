# -*- coding: utf-8-

import json
from typing import Dict, List, Type
from abc import ABCMeta, abstractmethod

from lib.common.iface import IQueue
from lib.common.iface import IThreadManager


EventNameType = str


__all__ = [
    "EventManager",
    "EventBase",
    "IEventHandler"
]


class QueueEvent:
    def __init__(self, name: EventNameType, arguments: dict):
        self.name = name
        self.arguments = arguments

    def generate_str_msg(self) -> str:
        return json.dumps(self.__dict__)


class EventBase(object, metaclass=ABCMeta):
    """ 事件 """
    name: EventNameType = None

    @property
    def arguments(self) -> dict:
        res = self.__dict__.copy()
        res.pop('name', None)
        return res

    @property
    def raise_on_exception(self):
        return False

    @abstractmethod
    def __init__(self, *args, **kwargs):
        # define event arguments in sub class
        pass

    def build_queue_event(self) -> QueueEvent:
        return QueueEvent(self.name, self.arguments)


class IEventHandler(object, metaclass=ABCMeta):
    """ 事件处理器 """
    @classmethod
    @abstractmethod
    def handle(cls, e: EventBase):
        # handle event using arguments kept in event
        raise NotImplementedError


class EventManager:
    """ 事件中心

    注册需要监听的事件和对应的事件处理器，在事件被触发时，会自动调用事件处理器处理事件
    """
    def __init__(self, queue_mgr: IQueue, thread_mgr: IThreadManager):
        self.__queue = queue_mgr
        self.__thread_mgr = thread_mgr
        self.__registered_events: Dict[EventNameType, Type[EventBase]] = {}
        self.__registered_event_handlers: Dict[EventNameType, Type[IEventHandler]] = {}

    def register(self, e: Type[EventBase], h: Type[IEventHandler]):
        self.__registered_events[e.name] = e
        self.__registered_event_handlers[e.name] = h

    def start_listen_loop(self):
        """ 开始循环监听和处理事件 """
        while True:
            queue_events = self.__fetch_events()
            for qe in queue_events:
                if self.__is_event_registered(qe.name):
                    e = self.__build_event_by_queue_event(qe)
                    self.__dispatch_event(e)

    def emit(self, e: EventBase):
        qe = e.build_queue_event()
        self.__queue.push(qe.generate_str_msg())

    def dispatch_event(self, e: EventBase):
        """ 分发事件 """
        self.__dispatch_event(e)

    def __is_event_registered(self, name: EventNameType) -> bool:
        return name in self.__registered_events and name in self.__registered_event_handlers

    def __fetch_events(self) -> List[QueueEvent]:
        """ 获取事件队列中的所有队列事件 """
        res = []
        for msg in self.__queue.pop_or_block():
            try:
                qe_json = json.loads(str(msg))
            except:
                print(f'lib event load msg failed: ,{msg}')
                return []

            qe = QueueEvent(name=qe_json.pop('name'), arguments=qe_json)
            res.append(qe)
        return res

    def __build_event_by_queue_event(self, qe: QueueEvent) -> EventBase:
        """ 根据队列事件构造事件 """
        event_class = self.__get_event_by_event_name(qe.name)
        return event_class(**qe.arguments)

    def __dispatch_event(self, e: EventBase):
        """ 分发事件 """
        handler = self.__get_event_handler_by_event_name(e.name)
        self.__thread_mgr.submit(handler.handle, e, raise_on_exception=e.raise_on_exception)

    def __get_event_handler_by_event_name(self, name: EventNameType) -> Type[IEventHandler]:
        """ 根据事件名称获取事件处理器 """
        return self.__registered_event_handlers.get(name)

    def __get_event_by_event_name(self, name: EventNameType) -> Type[EventBase]:
        """ 根据事件名称获取事件类型 """
        return self.__registered_events.get(name)
