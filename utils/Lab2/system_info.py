# -*- coding: utf-8 -*-

# @Time : 2019/12/7 23:10
# @Author : SeptemberHX
# @File : system_info.py
# @Description:


import requests
import time
import datetime

from utils.common.logger import get_logger

logger = get_logger('system_info')


def start_gather_system_info():
    while True:
        r = requests.post('http://3.131.111.217:46831/mserver/systemInfo', json={})
        print(r.json())
        logger.info(r.json())
        time.sleep(10)


if __name__ == '__main__':
    start_gather_system_info()
