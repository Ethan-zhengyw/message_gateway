# -*- coding: utf-8 -*-

from lib.common.iface.paginator import *


class Paginator(IPaginator):
    @staticmethod
    def __keep_idx_not_bigger_than_length(idx: int, length: int) -> int:
        if idx > length:
            return length
        else:
            return idx

    @classmethod
    def paging(cls, items: List[Any], paging_params: PagingParams) -> List[Any]:
        length = len(items)

        page = int(paging_params.page)
        limit = int(paging_params.limit)

        start = (page - 1) * limit
        start = cls.__keep_idx_not_bigger_than_length(start, length)

        end = start + limit
        end = cls.__keep_idx_not_bigger_than_length(end, length)

        return items[start:end]

