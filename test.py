import requests
import datetime
import random
from itertools import cycle
import time
from payment_system import answer
from multiprocessing.dummy import Pool


def final(address, trx_id=50, stop_func=50):
    address15021 = 'http://192.168.7.145:15021/api/external/status/'
    count = 1
    serial_numbers = ("90173073", "19032625", "01362152", "14828203", "03284023", "01924939")
    for serial_number in cycle(serial_numbers):
        print("============================================================================")
        print("count =", count)
        print("serial_number", serial_number)
        with requests.Session() as session:
            login = get_body("CMD_LOGIN", serial_number)
            response = session.post(address, json=login)
            print('Reply login--->', response.json())
            qr = get_body("CMD_GET_QR_CODE", serial_number, trx_id=trx_id)
            response = session.post(address, json=qr)
            print('GET_QR--->', response.json())
            term_id = response.json().get("terminal_id")
            merch_id = response.json().get("merchant_id")
            rrn = response.json().get("rrn")
            status_check = get_body("CMD_STATUS_CHECK", trx_id=trx_id, tid=term_id, mid=merch_id, rrn=rrn)
            response = session.post(address, json=status_check)
            print('Check_status--->', response.json())
            response_code = response.json().get('response_code')
            send_to_pre_host = answer(response.json().get('rrn'),
                                      response.json().get('merchant_id'),
                                      response.json().get('terminal_id'),
                                      int(qr.get('amount')),
                                      response.json().get('trx_id'))
            pool = Pool(2)
            with requests.Session() as answer_session:
                for f in [pool.apply_async(answer_session.post(address15021, json=send_to_pre_host)),
                          pool.apply_async(session.post(address, json={'msg_id': 'DELIVERY_REPORT', 'rrn': rrn}))]:
                    print(f)
                    response_code = '0'
                # if send_to_pre_host.get('status') == '0':
                #     print('entered')
                #     delivery_report = session.post(address, json={'msg_id': 'DELIVERY_REPORT', 'rrn': rrn})
                #     print('Delivery>>>', delivery_report.json())

                # print('PreHost>>>', pre_host.json())
            if response_code == 1000:
                for i in range(4):
                    time.sleep(2)
                    body = get_body("CMD_STATUS_CHECK", trx_id=trx_id, tid=term_id, mid=merch_id, rrn=rrn)
                    response = session.post(address, json=body)
                    print('Check_status--->', response.json())
                    response_code = response.json().get('response_code')
                    if response_code != 1000:
                        print('RESPONSE CODE>>>', response_code)
                        break
                else:
                    body = get_body("CMD_REVERSAL", trx_id=trx_id, tid=term_id, mid=merch_id, rrn=rrn)
                    response = session.post(address, json=body)
                    print('Reversal--->', response.json())
            else:
                print('response_code--->', response_code)
            count += 1
            stop_func -= 1
            trx_id += 1
            if stop_func == 0:
                break


def get_body(command_name: str, serial_number: str = None, trx_id=None, tid=None, mid=None, rrn=None):
    if command_name == "CMD_LOGIN":
        return {"msg_id": "CMD_LOGIN", "serial_number": serial_number}

    elif command_name == "CMD_GET_QR_CODE":
        amount = random.choices(["30000", "7800", "40000", "100000", "70000", "25000"])[0]
        return {"msg_id": "CMD_GET_QR_CODE",
                "date": str(datetime.datetime.now().strftime("%y%m%d%H%M%S")),
                "qr_type": 1, "serial_number": serial_number, "trx_type": 0, "trx_id": trx_id,
                "currency": 51, "amount": amount}

    elif command_name == "CMD_STATUS_CHECK":
        return {"msg_id": "CMD_STATUS_CHECK", "trx_type": 0, "trx_id": trx_id,
                "terminal_id": tid, "merchant_id": mid, "rrn": rrn}

    elif command_name == "CMD_REVERSAL":
        time.sleep(0.5)
        return {"msg_id": "CMD_REVERSAL", "trx_type": 10, "trx_id": trx_id,
                "date": str(datetime.datetime.now().strftime("%y%m%d%H%M%S")),
                "terminal_id": tid,
                "merchant_id": mid,
                "rrn": rrn}

