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
        'end': 300,
        'gateway': '144.34.200.189:8081'
    },
    '54.183.222.189': {
        'start': 300,
        'end': 600,
        'gateway': '144.34.160.60:8081'
    },
    '54.193.56.149': {
        'start': 600,
        'end': 900,
        'gateway': '144.34.214.165:8081'
    },
    '54.153.114.17': {
        'start': 900,
        'end': 1200,
        'gateway': '144.34.172.167:8081'
    },
    '13.57.111.205': {
        'start': 1200,
        'end': 1500,
        'gateway': '104.225.148.205:8081'
    },
    '54.183.133.108': {
        'start': 1500,
        'end': 1800,
        'gateway': '66.42.98.44:8081'
    },
    '52.53.235.188': {
        'start': 1800,
        'end': 2100,
        'gateway': '8.3.29.104:8081'
    },
    '54.193.48.236': {
        'start': 2100,
        'end': 2400,
        'gateway': '144.202.113.140:8081'
    },
    '54.67.105.1': {
        'start': 2400,
        'end': 2700,
        'gateway': '149.28.80.33:8081'
    },
    '54.67.58.146': {
        'start': 2700,
        'end': 3000,
        'gateway': '140.82.20.242:8081'
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