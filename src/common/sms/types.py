# -*- coding: utf-8 -*-

import datetime
import uuid

from ex_dataclass import ex_dataclass, field, EXpack

LIMIT_TYPE = str
LIMIT_TYPE_API = 'api'
LIMIT_TYPE_TEL = 'tel'
LIMIT_WINDOW = 1
API_LIMIT = 10
TEL_LIMIT = 1


@ex_dataclass
class SendReqTemplateParam(EXpack):
    title: str = field(default_factory=str)
    content: str = field(default_factory=str)


@ex_dataclass
class SendResp(EXpack):
    res_code: str = field(default_factory=str)
    res_message: str = field(default_factory=str)


@ex_dataclass
class SendReq(EXpack):
    qos: str = field(default_factory=str)
    acceptor_tel: str = field(default_factory=str)
    template_param: SendReqTemplateParam = field(default_factory=SendReqTemplateParam)
    timestamp: str = field(default_factory=str)
    id: str = field(default_factory=str)
    retry: int = field(default_factory=int)

    @classmethod
    def create(cls, qos: str, acceptor_tel: str, title: str, content: str) -> "SendReq":
        result = cls()
        result.qos = qos
        result.acceptor_tel = acceptor_tel
        result.template_param = SendReqTemplateParam(title=title, content=content)
        result.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result.id = str(uuid.uuid4())
        result.retry = 1
        return result

    def get_and_incr_retry(self) -> int:
        result = self.retry
        self.retry = result * 2
        if self.retry > 10:
            self.retry = 10
        return result
