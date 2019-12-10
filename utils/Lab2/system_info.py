# -*- coding: utf-8 -*-

# @Time : 2019/12/7 23:10
# @Author : SeptemberHX
# @File : system_info.py
# @Description:


import requests
import time
import datetime


def start_gather_system_info():
    while True:
        r = requests.post('http://3.136.80.127:9001/mserver/systemInfo', json={})
        print(datetime.datetime.now().timestamp())
        print(r.json())
        time.sleep(10)

if __name__ == '__main__':
    start_gather_system_info()
