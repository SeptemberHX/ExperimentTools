# -*- coding: utf-8 -*-

# @Time : 2019/12/3 15:09
# @Author : SeptemberHX
# @File : requst_simulation.py
# @Description:

import requests, json, datetime


def do_request(url, data_size_in_kb):
    start_time = datetime.datetime.now().timestamp() * 1000  # mills
    r = requests.post(url, json={
        'valueMap': {
            'interval': 0
        }
    })
    end_time = datetime.datetime.now().timestamp() * 1000
    interval = r.json()['valueMap']['interval']
    response_time = end_time - start_time - interval
    print(response_time)


if __name__ == '__main__':
    do_request('http://144.34.200.189:8080/pay', 10)
