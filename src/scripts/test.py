import random
import time

from ex_dataclass import ex_dataclass, field, EXpack

import common.requests as ur
import common.static as const

title = 't1'
content = 'c1'
session_id = '22aab8ce-2ffe-45bf-8039-3c92f7e5418a'

success = 0
fail = 0


@ex_dataclass
class Case(EXpack):
    tel: str = field(default_factory=str)
    qos: str = field(default_factory=str)
    title: str = field(default_factory=str)
    content: str = field(default_factory=str)


def generate_test_case():
    result = []
    for j in range(50):
        # tel = tels[random.randint(0, 4)]
        tel = random.randint(1000, 1000000)
        for k in range(3):
            qos = random.randint(1, 3)
            result.append(Case(tel=tel, qos=qos, title=title, content=content))
    return result


for case in generate_test_case():
    url = f'http://localhost:8888/directmessage?' \
        f'tels={case.tel}&qos={case.qos}&userName=admin&sessionId={session_id}'
    data = dict(
        title=case.title,
        content=case.content
    )
    resp = ur.post(url, json=data, headers=const.JSON_HEADER)
    if resp.status_code == 200:
        success += 1
    else:
        fail += 1
    time.sleep(1)


print('success', success)
print('fail', fail)
