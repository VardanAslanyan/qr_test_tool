import datetime
import random

count_trx_id = 1


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
                       'transaction_id': f'{datetime.datetime.now().strftime("%Y%m%d")}'
                                         f'{"0"*(7 - len(str(count_trx_id)))}{count_trx_id}',
                       'bankname': bankname
                       }
            }
    return body


count_trx_id += 1