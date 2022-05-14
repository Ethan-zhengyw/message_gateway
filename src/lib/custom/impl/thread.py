# -*- coding: utf-8 -*-

from typing import Callable

from flask import current_app
from lizhi_service.app import LizhiApp

from lib.common.iface import IThreadManager

app: LizhiApp = current_app


class FakeThreadManager(IThreadManager):
    """ 假的线程管理器，不采用线程机制调用方法，而是以直接同步阻塞的方式调用

    Q：为什么会有这样的需要？
    A：
    刚开始实践DDD时，依照书本所述——"子领域之间，应该通过消息机制进行异步通信"，创建了简单的事件中心，
    供注册领域事件和事件处理器，在必要时发送领域事件，触发事件处理器执行事件处理函数。

    而目前系统当前的功能中涉及的领域事件，没有太大异步化的必要性，但是因为采用事件驱动的方式进行编程，
    有助于在代码层面明确领域事件，以及其对应的处理子过程，有助于代码的可维护性，所以为了受用事件驱动编程的好处，就有了
    "假的线程管理器"的需要。
    """
    @classmethod
    def submit(cls, func: Callable, *args, raise_on_exception=False, **kwargs):
        func(*args, **kwargs)
