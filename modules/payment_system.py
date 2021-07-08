import datetime
import random


def answer(rrn, mid, tid, amount, transaction_id, bankname='FPS'):
    status = random.choices(['0', '116', '109'])[0]  # TODO PreHost not work with response code 109
    body = {'version': '1.0',
            'method': 'status',
            'id': str(transaction_id),
            'params': {'rrn': rrn,
                       'mid': mid,
                       'tid': tid,
                       'amount': amount,
                       'currency': '051',
                       'datetime': datetime.datetime.now().isoformat().replace('T', ' ')[:19],
                       'status': status,
                       'transaction_id': f'{datetime.datetime.now().strftime("%Y%m%d")}0'
                                         f'{datetime.datetime.now().strftime("%H%M%S")}',
                       'bankname': bankname
                       }
            }
    return body
