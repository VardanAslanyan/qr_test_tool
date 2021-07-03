import requests
import datetime
import random


def answer(rrn, mid, tid, amount, transaction_id, bankname='MobiDram'):
    address = 'http://192.168.7.145:15021/api/external/status/'
    status = random.choices(['000', '116', '109'])[0]
    body = {'version': '1.0',
            'method': 'status',
            'id': '12',
            'params': {'rrn': rrn,
                       'mid': mid,
                       'tid': tid,
                       'amount': amount,
                       'currency': '051',
                       'datetime': '2021-07-04 02:10:00',
                       'status': '000',
                       'transaction_id': transaction_id,
                       'bankname': bankname
                       }
            }
    print('BODY--->', body)
    with requests.Session() as session:
        response = session.post(address, json=body)
        print('Response from PreHost--->', response.json())
