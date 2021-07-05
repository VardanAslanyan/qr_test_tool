import requests
import datetime
import random
from itertools import cycle
import time
from payment_system import answer
from multiprocessing.dummy import Pool
import asyncio


def final(address, trx_id=1, stop_func=50):
    address15021 = 'http://192.168.7.145:15021/api/external/status/'
    count = 1
    serial_numbers = ("01924939", "19032625", "01362152", "14828203", "03284023", "90173073")
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
            delivery = {'msg_id': 'DELIVERY_REPORT', 'rrn': rrn}
            # pool = Pool(3)
            with requests.Session() as answer_session:
                test = ((send_to_pre_host, address15021, answer_session),
                        (status_check, address, session),
                        (delivery, address, session))
                res1, res2, res3 = asyncio.get_event_loop().run_until_complete(multiple_tasks(test))
                # loop = asyncio.get_event_loop()
                # count_pool = 1
                # for i, j, k in test:
                #     print(i)
                    # print(count_pool)
                    ### loop.run_in_executor(None, internet_resource_getter, i)
                    # asyncio.run(internet_resource_getter(i, j, k))
                    # count_pool += 1
                # for f in [pool.apply_async(answer_session.post(address15021, json=send_to_pre_host)),
                #           pool.apply_async(session.post(address, json=status_check)),
                #           pool.apply_async(session.post(address, json=delivery))]:
                #     print(f.wait())
                response_code = '0'
                # if send_to_pre_host.get('status') == '0':
                #     print('entered')
                #     delivery_report = session.post(address, json={'msg_id': 'DELIVERY_REPORT', 'rrn': rrn})
                #     print('Delivery>>>', delivery_report.json())
                # mid >>> 340003274, tid >>> 34063274, serial >>> 01924939
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


async def internet_resource_getter(post_data, base_uri, session):
    print('TEST>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    stuff_got = []
    response = session.post(base_uri, json=post_data)
    await response.json()
    stuff_got.append(response.json())
    print('stuff_got', stuff_got)
    return stuff_got


async def test_1(test):
    res1 = await test[0][2].post(test[0][1], json=test[0][0])
    return res1


async def test_2(test):
    res2 = await test[1][2].post(test[1][1], json=test[1][0])
    return res2

async def test_3(test):
    res3 = await test[2][2].post(test[2][1], json=test[2][0])
    return res3


async def multiple_tasks(test):
    input_coroutines = [test_1(test), test_2(test), test_3(test)]
    res = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return res




