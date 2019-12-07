# -*- coding: utf-8 -*-

# @Time : 2019/12/7 16:04
# @Author : SeptemberHX
# @File : controller.py
# @Description:

import sys
import requests


ip_list = {
    '13.57.224.106': {
        'start': 0,
        'end': 0,
        'gateway': 0
    },
    '54.183.222.189': {
        'start': 0,
        'end': 0,
        'gateway': 0
    },
    '54.193.56.149': {
        'start': 0,
        'end': 0,
        'gateway': 0
    },
    '54.153.114.17': {
        'start': 0,
        'end': 0,
        'gateway': 0
    },
    '13.57.111.205': {
        'start': 0,
        'end': 10,
        'gateway': '144.34.200.189:8081'
    },
    '54.183.133.108': {
        'start': 0,
        'end': 0,
        'gateway': 0
    },
    '52.53.235.188': {
        'start': 0,
        'end': 0,
        'gateway': 0
    },
    '54.193.48.236': {
        'start': 0,
        'end': 0,
        'gateway': 0
    },
    '54.67.105.1': {
        'start': 0,
        'end': 0,
        'gateway': 0
    },
    '54.67.58.146': {
        'start': 0,
        'end': 0,
        'gateway': 0
    },
}
simulation_port = 54321


def init_simulator():
    for ip in ip_list:
        try:
            response = requests.post('http://{0}:{1}/load'.format(ip, simulation_port), json=ip_list[ip])
            if response.status_code == 200:
                print('Success init simulator on {0}'.format(ip))
        except Exception as e:
            print('Fail to init simulator on {0}'.format(ip))


def start_simulator():
    for ip in ip_list:
        try:
            response = requests.get('http://{0}:{1}/start'.format(ip, simulation_port))
            if response.status_code == 200:
                print('Success start simulator on {0}'.format(ip))
        except Exception as e:
            print('Fail to start simulator on {0}'.format(ip))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(sys.argv[0], 'init|start')
        exit(0)
    if sys.argv[1] == 'init':
        init_simulator()
    elif sys.argv[1] == 'start':
        start_simulator()