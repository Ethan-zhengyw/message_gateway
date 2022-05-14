# -*- coding: utf-8 -*-

import json

import common.static as const
from common.sms.client import SmsClient, SendReq
from service.auth import location_auth_wrapper
from .vm import request_parser


@location_auth_wrapper(location='args')
def directmessage():
    args = request_parser.parse_args()
    sms_req = SendReq.create(
        qos=args['qos'], acceptor_tel=args['tels'], title=args['title'], content=args['content'])

    SmsClient.async_send(sms_req)
    # SmsClient.send(sms_req)

    return json.dumps({'code': 200, 'message': 'success'}), 200, const.JSON_HEADER

