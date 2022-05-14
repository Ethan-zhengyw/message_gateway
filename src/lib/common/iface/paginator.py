# -*- coding: utf-8 -*-

from typing import List, Any
from abc import abstractmethod, ABCMeta
from ex_dataclass import ex_dataclass, field


DEFAULT_PAGE = 1
DEFAULT_LIMIT = 10


@ex_dataclass
class PagingParams:
    page: int = field(default=DEFAULT_PAGE)
    limit: int = field(default=DEFAULT_LIMIT)


class IPaginator(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def paging(cls, items: List[Any], paging_params: PagingParams) -> List[Any]:
        raise NotImplementedError
