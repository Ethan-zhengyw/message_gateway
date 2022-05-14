# -*- coding: utf-8 -*-

from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from common.log import get_logger

wrap_view_pre = '_AutoGen'
logger = get_logger('service:common:route')


def route_set(_api, *urls, **kwargs):
    """ """
    def _wrap(cls):
        cls._init_route_set(_api, urls, **kwargs)
        return cls
    return _wrap


def wrap_view(_api, *urls, name=None, method=None, base_cls=Resource):
    """
    sample:
        @wrap_view(_api, '/clusters/fetch_old_db1/')
        @login_check
        @_api.expect(id_args)
        @wrap_log
        def post(self):
            pass
    """

    def _wrap(view_func):
        method_name = view_func.__name__ if method is None else method
        methods = {method_name.lower(): view_func}
        methods['methods'] = set(methods.keys())
        if name is None:
            ns = urls[0].split('/')
        else:
            ns = name.split('_')
        new_cls = type(
            '%s%sRes' % (wrap_view_pre, ''.join([n.capitalize() for n in ns if n])),
            (base_cls, ),
            methods,
            )
        _api.route(*urls)(new_cls)
        return new_cls
    return _wrap


class ResourceSetMixin(object):
    """ 资源集
    支持多url多route方法, 需要配合 route_set, route 使用
    sample:

@route_set(api, '/echo1/')
class Echo1(ResourceSet):
    cls_property1 = 'test'

    @api.expect(parser_echo1)
    def post(self):
        return {'now': datetime.datetime.now(), 'data': request.args}

    @route('/echo1/echo1', method='POST')
    @api.expect(make_params('msg'))
    def echo1(self):
        return {'now': datetime.datetime.now(), 'data': request.args}

     """
    route_urls_key = '_route_urls_'
    route_clses = {}  # {url: customCls}
    root_urls = None

    control = None  # 控制类

    @classmethod
    def _fix_func_urls(cls, func):
        """ 判断是否相对路径，是的话添加父urls前缀
        :return method, urls
            urls: List[str],
                支持相对路径： 如：urls = ['abc/'], route_set时urls=['/root/'], 那最终urls = ['/root/abc/']
                支持后缀自动添加函数名：如：urls = ['/abc'] wrap的方法是func, 最终urls = ['/abc/func/']
        """
        from posixpath import join, sep
        if not hasattr(func, cls.route_urls_key):
            return None, None
        method, urls, raw_url = getattr(func, cls.route_urls_key)
        result = []
        root_urls = cls.root_urls
        func_name = func.__name__

        def _add_url(_url):
            if _url in ['', '/', None]:
                _url = sep + func_name + sep
            elif not _url.endswith(sep) and not raw_url:
                _url = join(_url, func_name) + sep
            result.append(_url)

        for url in urls:
            if url.startswith(sep):
                _add_url(url)
                continue
            for r_url in root_urls:
                if url == '':
                    _add_url(r_url if r_url in [None, '', '/'] or r_url[-1] != sep else r_url[:-1])
                else:
                    _add_url(join(r_url, url))
        return method, result

    @classmethod
    def _init_route_set(cls, api, urls, **kwargs):
        cls.root_urls = urls
        if urls:
            api.route(*urls, **kwargs)(cls)

        for name in dir(cls):
            func = getattr(cls, name)
            method, urls = cls._fix_func_urls(func)
            if not urls:
                continue
            sub_cls = wrap_view(api, *urls, method=method, base_cls=cls)(func)
            key = '%s_%s%s' % (name, api.path, urls[0])
            # todo swagger不支持, 实际url是可以请求到的
            # key = '%s%s' % (api.path, urls[0])
            # if key in cls.route_clses:
            #     # route包装的方法,如果使用了相同的url，之前的会被覆盖掉，暂时没想到办法解决，先抛出异常
            #     raise ValueError('no support double same url(%s) by two func(%s)' % (key, name))
            cls.route_clses[key] = sub_cls

    @classmethod
    def ctl_op_prepare(cls, op_func, kwargs):
        if hasattr(op_func, '__self__'):
            ctl_cls = op_func.__self__
            func = op_func
        else:
            ctl_cls = cls.control
            func = getattr(ctl_cls, op_func)
        return ctl_cls, func

    @classmethod
    def ctl_op(cls, op_func, parser):
        kwargs = parser.parse_args()
        ctl_cls, func = cls.ctl_op_prepare(op_func, kwargs)
        ok, msg = func(**kwargs)
        if not ok:
            logger.info('view_op cls(%s) op_name(%s) fail: %s', ctl_cls, op_func, msg)
            raise BadRequest(msg)
        return msg


class ResourceSet(ResourceSetMixin, Resource):
    pass

