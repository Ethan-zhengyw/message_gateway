# -*- coding: utf-8 -*-

import json
import time

import common.requests as ur
import common.static as const
from common.config import ConfigHelper
from common.log import get_logger
from common.redis import helper
from .limiter import typed_rate_limit_wrapper, RateLimitExceeded
from .types import *

logger = get_logger('common:sms:client')


class SmsClient:
    @classmethod
    def async_send(cls, msg: SendReq):
        queue_key = cls.__get_message_queue_key(msg.qos)
        helper.client.lpush(queue_key, json.dumps(msg.asdict()))
        print(f'{msg.id} async_sent, key: {queue_key}, details: {msg}')
        resp_redis_key = cls.__get_message_resp_redis_key(msg.id)
        # print('waiting', msg.id)
        resp = helper.client.get(resp_redis_key)
        while resp is None:
            time.sleep(const.WAIT_TIME)
            # print('waiting', msg.id)
            resp = helper.client.get(resp_redis_key)
        print(f'{msg.id} finished.')

    @classmethod
    @typed_rate_limit_wrapper(LIMIT_TYPE_API)
    @typed_rate_limit_wrapper(LIMIT_TYPE_TEL)
    def send(cls, msg: SendReq) -> SendResp:
        headers = {
            'Content-Type': 'application/json'
        }

        url = f'http://{ConfigHelper.get_mock_server_endpoint()}/v2/emp/templateSms/sendSms'
        data = msg.asdict()
        data.pop('id')
        resp = ur.post(url, json=data, headers=headers).json()
        print(json.dumps(resp))
        send_resp = SendResp(**resp)
        return send_resp

    @classmethod
    def consume(cls, qos: int):
        """ 从指定优先级队列中读取消息并发送 """
        queue_key = cls.__get_message_queue_key(qos)
        helper.client.delete(queue_key)

        print(f'sms consume started, qos: {qos}')
        while True:
            # print(f'popping {queue_key}')
            message = helper.client.rpop(queue_key)
            if not message:
                # time.sleep(1)
                time.sleep(const.WAIT_TIME)
                continue
            print(f'{message} popped, decoding...')
            msg = SendReq(**json.loads(message))
            print(f'{msg.id} popped.')
            try:
                resp = cls.send(msg)
                resp_key = cls.__get_message_resp_redis_key(msg.id)
                if resp.res_code == "0":
                    helper.client.set(resp_key, json.dumps(resp.asdict()))
                    print(f'{msg.id} sent.')
                else:
                    print(f'{msg.id} failed, {resp}, sleeping: {msg.retry}')
                    # time.sleep(msg.get_and_incr_retry())
                    time.sleep(const.WAIT_TIME)
                    print(f'{msg.id} pushed again in retry')
                    helper.client.lpush(queue_key, json.dumps(msg.asdict()))
            except RateLimitExceeded:
                # 本地已出发限流，没有调用sms，加入队列等待重新执行
                print(f'{msg.id} limited, sleeping: {msg.retry}')
                time.sleep(const.WAIT_TIME)
                # time.sleep(msg.get_and_incr_retry())
                print(f'{msg.id} pushed again in limit')
                helper.client.lpush(queue_key, json.dumps(msg.asdict()))

    @classmethod
    def __get_message_resp_redis_key(cls, message_id: str) -> str:
        return f'{const.APP_NAME}_msg_resp_{message_id}'

    @classmethod
    def __get_message_queue_key(cls, qos) -> str:
        return f'{const.APP_NAME}_msg_queue_qos{qos}'
