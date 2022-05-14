# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor

from flask import Flask

from common.sms.client import SmsClient
from service.auth import view as auth_view
from service.directmessage import view as message_view

app = Flask(__name__)
thread_pool = ThreadPoolExecutor(max_workers=10)


@app.route("/directmessage", methods=['POST'])
def directmessage():
    return message_view.directmessage()


@app.route("/auth/user/register", methods=['POST'])
def register():
    return auth_view.register()


@app.route("/auth/user/login", methods=['POST'])
def login():
    return auth_view.login()


@app.route("/auth/user/logout", methods=['POST'])
def logout():
    return auth_view.logout()


def start_consumes():
    for i in range(6):
        thread_pool.submit(SmsClient.consume, qos=1)

    for i in range(3):
        thread_pool.submit(SmsClient.consume, qos=2)

    for i in range(1):
        thread_pool.submit(SmsClient.consume, qos=3)


if __name__ == '__main__':
    start_consumes()
    app.run(host='0.0.0.0', port=80)
