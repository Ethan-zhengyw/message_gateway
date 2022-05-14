# -*- coding: utf-8 -*-
import common.static as const
import json
import service.auth.vm as vm
from . import UserMgr, location_auth_wrapper


def register():
    args = vm.create_user_parser.parse_args()
    UserMgr.create_user(args['userName'], args['password'])
    return json.dumps({'code': 200, 'message': 'success'}), 200, const.JSON_HEADER


def login():
    args = vm.login_parser.parse_args()
    session_id = UserMgr.login(args['userName'], args['password'])
    return json.dumps({'code': 200, 'message': 'success', 'sessionId': session_id}), 200, const.JSON_HEADER


@location_auth_wrapper(location='json')
def logout():
    args = vm.logout_parser.parse_args()
    UserMgr.logout(args['userName'])
    return json.dumps({'code': 200, 'message': 'success'}), 200, const.JSON_HEADER
