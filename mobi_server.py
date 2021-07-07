import json
import requests


address15021 = 'http://192.168.7.145:15021/api/external/status/'

with open('response.txt', 'r') as resp:
    send_to_pre_host = json.load(resp)
print('OUT>>>>>>>>>>', send_to_pre_host)

with requests.Session() as send_answer:
    to_qr_host = send_answer.post(address15021, json=send_to_pre_host)
    print(to_qr_host.json())
