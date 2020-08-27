# -*- coding: utf-8 -*-

# @Time : 2019/12/7 16:04
# @Author : SeptemberHX
# @File : controller.py
# @Description:

import requests
import datetime
import time


ip_list = {
    '18.162.50.165': {
        'start': 0,
        'end': 200,
        'gateway': '18.162.50.165:8081'
    },
    '18.166.154.73': {
        'start': 200,
        'end': 400,
        'gateway': '18.166.154.73:8081'
    },
    '18.166.152.44': {
        'start': 400,
        'end': 600,
        'gateway': '18.166.152.44:8081'
    },
    '18.162.154.133': {
        'start': 600,
        'end': 800,
        'gateway': '18.162.154.133:8081'
    },
    '18.166.31.147': {
        'start': 800,
        'end': 1000,
        'gateway': '18.166.31.147:8081'
    },
    '18.162.48.228': {
        'start': 1000,
        'end': 1200,
        'gateway': '18.162.48.228:8081'
    },
    '18.162.152.1': {
        'start': 1200,
        'end': 1400,
        'gateway': '18.162.152.1:8081'
    },
    '18.162.111.22': {
        'start': 1400,
        'end': 1600,
        'gateway': '18.162.111.22:8081'
    },
    '18.163.100.25': {
        'start': 1600,
        'end': 1800,
        'gateway': '18.163.100.25:8081'
    },
    '18.166.115.92': {
        'start': 1800,
        'end': 2000,
        'gateway': '18.166.115.92:8081'
    },
}
simulation_port = 54321


def init_simulator():
    for ip in ip_list:
        try:
            json_data = {
                'start': ip_list[ip]['start'] / 3,
                'end': ip_list[ip]['end'] / 3,
                'gateway': ip_list[ip]['gateway']
            }
            response = requests.post('http://{0}:{1}/load'.format(ip, simulation_port), json=json_data)
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


def reset_gateway():
    for ip in ip_list:
        try:
            response = requests.get('http://{0}/reset'.format(ip_list[ip]['gateway']))
            if response.status_code == 200:
                print('Success reset gateway on {0}'.format(ip_list[ip]['gateway']))
        except Exception as e:
            print('Failed to reset gateway on {0}'.format(ip_list[ip]['gateway']))



def evolve():
    count = 1
    while True:
        try:
            print(count)
            response = requests.get('http://3.131.111.217:46831/mserver/evolve?type=1')
            time.sleep(330)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    reset_gateway()
    init_simulator()
    print(datetime.datetime.now().timestamp())
    start_simulator()
    evolve()