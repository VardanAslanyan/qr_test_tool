import datetime
import random


def answer(rrn, mid, tid, amount, transaction_id, bankname='MobiDram'):

    status = random.choices(['0', '116', '109'])[0]
    body = {'version': '1.0',
            'method': 'status',
            'id': str(transaction_id),
            'params': {'rrn': rrn,
                       'mid': mid,
                       'tid': tid,
                       'amount': amount,
                       'currency': '051',
                       'datetime': datetime.datetime.now().isoformat().replace('T', ' ')[:19],
                       'status': '0',
                       'transaction_id': str(datetime.datetime.now().strftime("%y%m%d%H%M%S")),
                       'bankname': bankname
                       }
            }
    print('BODY--->', body)

    return body


