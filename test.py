import requests
import datetime
import random
from itertools import cycle
import time


def final(address, trx_id=50, stop_func=50):
    count = 1
    serial_numbers = ("90173073", "19032625", "01362152", "14828203", "03284023", "01924939")
    for serial_number in cycle(serial_numbers):
        print("============================================================================")
        print("count =", count)
        print("serial_number", serial_number)
        with requests.Session() as session:
            body = get_body("CMD_LOGIN", serial_number)
            response = session.post(address, json=body)
            print('Reply login--->', response.json())
            body = get_body("CMD_GET_QR_CODE", serial_number, trx_id=trx_id)
            response = session.post(address, json=body)
            print('GET_QR--->', response.json())
            term_id = response.json().get("terminal_id")
            merch_id = response.json().get("merchant_id")
            rrn = response.json().get("rrn")
            body = get_body("CMD_STATUS_CHECK", trx_id=trx_id, tid=term_id, mid=merch_id, rrn=rrn)
            response = session.post(address, json=body)
            print('Check_status--->', response.json())
            if response.json().get('response_code') == 1000:
                for i in range(4):
                    body = get_body("CMD_STATUS_CHECK", trx_id=trx_id, tid=term_id, mid=merch_id, rrn=rrn)
                    response = session.post(address, json=body)
                    print('Check_status--->', response.json())

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

