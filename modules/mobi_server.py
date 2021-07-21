import requests


def main(to_host):
    print('Request to PreHost', to_host)
    address15021 = 'http://192.168.7.145:15021/api/external/status/'
    with requests.Session() as session_ps:
        with session_ps.post(address15021, json=to_host) as response:
            resp = response.json()
            print()
            print("-------------ANSWER_FROM_PreHost>>>>>>>>>:", resp)
            print()

