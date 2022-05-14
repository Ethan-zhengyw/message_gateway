# -*- coding: utf-8 -*-

from flask_restplus import reqparse
from werkzeug.routing import ValidationError


create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('userName', type=str, required=True, location="json")
create_user_parser.add_argument('password', type=str, required=True, location="json")

login_parser = create_user_parser

logout_parser = reqparse.RequestParser()
logout_parser.add_argument('userName', type=str, required=True, location="json")
logout_parser.add_argument('sessionId', type=str, required=True, location="json")



