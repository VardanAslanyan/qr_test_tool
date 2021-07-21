import datetime
import random


def answer(rrn, mid, tid, amount, transaction_id):
    bankname = random.choice(['FPS', 'Evocabank', 'MobiDram', 'ConverseBank'])
    status = random.choice(['0', '5', '100', '103', '109', '116', '120', '904', '912', '913', '914', '923'])
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
                       'transaction_id': str(random.randint(1, 9999999999999)),
                       'bankname': bankname
                       }
            }
    return body
