import requests
import datetime
import random
from itertools import cycle
import time
from payment_system import answer
import json
import aiohttp
import asyncio
import threading


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
            send_to_pre_host = answer(response.json().get('rrn'),
                                      response.json().get('merchant_id'),
                                      response.json().get('terminal_id'),
                                      int(qr.get('amount')),
                                      response.json().get('trx_id'))

            # loop = asyncio.get_event_loop()
            # loop.run_in_executor(None, main, send_to_pre_host)     #run_until_complete(main(send_to_pre_host))

            # with open('response.txt', 'w') as to_pre:
            #     json.dump(send_to_pre_host, to_pre)
            # print(send_to_pre_host)

            thr = threading.Thread(target=main, args=(send_to_pre_host,))
            thr.start()  # Will run "foo"

            time.sleep(5)
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


def main(to_host):
    print('ASYNC')
    address15021 = 'http://192.168.7.145:15021/api/external/status/'
    with requests.Session() as session_ps:
        with session_ps.post(address15021, json=to_host) as response:
            html = response.json()
            print("Body:", html)

