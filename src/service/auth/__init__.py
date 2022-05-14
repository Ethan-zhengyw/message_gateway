# -*- coding: utf-8 -*-

import json
from uuid import uuid4

from flask import request
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotFound

import common.static as const
from common.redis import helper


class UserMgr:
    @classmethod
    def create_user(cls, name: str, pwd: str):
        if cls.__is_user_exist(name):
            raise BadRequest(f'user({name}) already exists.')
        pwd_key = cls.__get_user_pwd_key(name)
        helper.client.set(pwd_key, pwd)

    @classmethod
    def login(cls, name: str, pwd: str) -> str:
        if cls.__is_user_exist(name):
            if cls.__is_pwd_match_name(name, pwd):
                session_key = cls.__get_user_session_key(name)
                session_id = str(uuid4())
                helper.client.set(session_key, session_id)
                return session_id
        else:
            raise NotFound(f'user({name}) not found.')

    @classmethod
    def logout(cls, name: str):
        session_key = cls.__get_user_session_key(name)
        helper.client.delete(session_key)

    @classmethod
    def is_session_id_match_name(cls, name: str, session_id: str) -> bool:
        session_key = cls.__get_user_session_key(name)
        session_id_kept = helper.client.get(session_key)
        return session_id == session_id_kept

    @classmethod
    def __is_pwd_match_name(cls, name: str, pwd: str) -> bool:
        pwd_key = cls.__get_user_pwd_key(name)
        pwd_kept = helper.client.get(pwd_key)
        return pwd == pwd_kept

    @classmethod
    def __is_user_exist(cls, name: str) -> bool:
        pwd_key = cls.__get_user_pwd_key(name)
        if helper.client.get(pwd_key):
            return True
        return False

    @classmethod
    def __get_user_pwd_key(cls, name: str) -> str:
        return f'{const.APP_NAME}_user_{name}_pwd'

    @classmethod
    def __get_user_session_key(cls, name: str) -> str:
        return f'{const.APP_NAME}_user_{name}_session'


def location_auth_wrapper(location: str):
    def auth_wrapper(func):
        def wrapped(*args, **kwargs):

            def __decode_name_and_session_id() -> (str, str):
                name_ = getattr(request, location, dict()).get('userName')
                session_id_ = getattr(request, location, dict()).get('sessionId')
                return name_, session_id_

            name, session_id = __decode_name_and_session_id()

            if name and session_id and UserMgr.is_session_id_match_name(name, session_id):
                return func(*args, **kwargs)
            else:
                return json.dumps({'code': 403, 'message': '禁止未经授权访问'}), 403, const.JSON_HEADER

        return wrapped
    return auth_wrapper
