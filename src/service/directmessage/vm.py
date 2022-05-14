# -*- coding: utf-8 -*-

from flask_restplus import reqparse
from werkzeug.routing import ValidationError


def validate_title(title):
    if len(title) < 1 or len(title) > 64:
        raise ValidationError('title 长度非法')

    return title


def validate_qos(qos):
    try:
        qos = int(qos)

        if qos not in (1, 2, 3):
            raise ValidationError('qos取值非法')

        return qos

    except TypeError:
        raise ValidationError('qos类型非法')


request_parser = reqparse.RequestParser()
request_parser.add_argument('tels', type=str, required=True, location="args")
request_parser.add_argument('qos', type=validate_qos, required=True, location="args")
request_parser.add_argument('userName', type=str, required=True, location="args")
request_parser.add_argument('sessionId', type=str, required=True, location="args")
request_parser.add_argument('title', type=validate_title, required=True, location="json")
request_parser.add_argument('content', type=str, required=True, location="json")


