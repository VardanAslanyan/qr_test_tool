import requests
from itertools import cycle
import time
from .payment_system import answer
import threading
from .mobi_server import main
from .command_body import get_body


def final(address, trx_id=1, stop_func=50):
    count = 1
    serial_numbers = ("01924939", "19032625", "01362152", "14828203", "03284023", "90173073")
    for serial_number in cycle(serial_numbers):
        print("============================================================================")
        print("count =", count)
        print("serial_number", serial_number)
        with requests.Session() as session:
            login = get_body("CMD_LOGIN", serial_number)
            login_response = session.post(address, json=login)
            print('Reply login--->', login_response.json())
            qr = get_body("CMD_GET_QR_CODE", serial_number, trx_id=trx_id)
            get_qr_response = session.post(address, json=qr)
            print('GET_QR--->', get_qr_response.json())
            term_id = get_qr_response.json().get("terminal_id")
            merch_id = get_qr_response.json().get("merchant_id")
            rrn = get_qr_response.json().get("rrn")
            status_check = get_body("CMD_STATUS_CHECK", trx_id=trx_id, tid=term_id, mid=merch_id, rrn=rrn)
            response = session.post(address, json=status_check)
            print('Check_status--->', response.json())
            count_trx_id = 1
            send_to_pre_host = answer(response.json().get('rrn'),
                                      response.json().get('merchant_id'),
                                      response.json().get('terminal_id'),
                                      int(qr.get('amount')),
                                      response.json().get('trx_id'))
            thr = threading.Thread(target=main, args=(send_to_pre_host,))
            thr.start()
            count_trx_id += 1
            time.sleep(3)
            for j in range(4):
                status_check = get_body("CMD_STATUS_CHECK", trx_id=trx_id, tid=term_id, mid=merch_id, rrn=rrn)
                status_response = session.post(address, json=status_check)
                print('Check_status--->', status_response.json())
                response_code = status_response.json().get('response_code')
                if response_code == 0:
                    delivery = {'msg_id': 'DELIVERY_REPORT', 'rrn': rrn}
                    del_send = session.post(address, json=delivery)
                    print('DELIVERY_REPORT', del_send.json())
                    break
                elif response_code == 1000:
                    time.sleep(2)
                    continue
                else:
                    print('RESPONSE CODE>>>', response_code)
                    break
            else:
                body = get_body("CMD_REVERSAL", trx_id=trx_id, tid=term_id, mid=merch_id, rrn=rrn)
                response = session.post(address, json=body)
                print('Reversal--->', response.json())
            count += 1
            stop_func -= 1
            trx_id += 1
            if stop_func == 0:
                break







