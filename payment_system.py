import datetime
import random


def answer(rrn, mid, tid, amount, transaction_id, bankname='FPS'):

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
                       'transaction_id': f'{datetime.datetime.now().strftime("%Y%m%d")}0000058',
                       'bankname': bankname
                       }
            }
    # print('BODY--->', body)

    return body


if __name__ == '__main__':
    #
    # import aiohttp
    # import asyncio
    # import ujson
    #
    #
    # async def main():
    #     async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
    #         async with session.post('http://httpbin.org/get', json={}) as resp:
    #             print(resp.status)
    #             print(await resp.json())
    #
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    import asyncio


    async def test_1(dummy):
        res1 = await foo1()
        return res1


    async def test_2(dummy):
        res2 = await foo2()
        return res2


    async def multiple_tasks(dummy):
        input_coroutines = [test_1(dummy), test_2(dummy)]
        res = await asyncio.gather(*input_coroutines, return_exceptions=True)
        return res

    dummy = 0
    res1, res2 = asyncio.get_event_loop().run_until_complete(multiple_tasks(dummy))