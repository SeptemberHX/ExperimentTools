# -*- coding: utf-8 -*-

# @Time : 2019/12/7 16:04
# @Author : SeptemberHX
# @File : controller.py
# @Description:

import requests
import datetime
import time


ip_list = {
    '18.166.75.39': {
        'start': 0,
        'end': 400,
        'gateway': '18.166.75.39:8081'
    },
    '18.166.29.246': {
        'start': 400,
        'end': 800,
        'gateway': '18.166.29.246:8081'
    },
    '18.162.141.195': {
        'start': 800,
        'end': 1200,
        'gateway': '18.162.141.195:8081'
    },
    '18.162.168.65': {
        'start': 1200,
        'end': 1600,
        'gateway': '18.162.168.65:8081'
    },
    '18.166.60.92': {
        'start': 1600,
        'end': 2000,
        'gateway': '18.166.60.92:8081'
    },
    '18.162.112.128': {
        'start': 2000,
        'end': 2400,
        'gateway': '18.162.112.128:8081'
    },
    '18.166.154.126': {
        'start': 2400,
        'end': 2800,
        'gateway': '18.166.154.126:8081'
    },
    '18.162.167.91': {
        'start': 2800,
        'end': 3200,
        'gateway': '18.162.167.91:8081'
    },
    '18.162.152.105': {
        'start': 3200,
        'end': 3600,
        'gateway': '18.162.152.105:8081'
    },
    '18.166.115.92': {
        'start': 3600,
        'end': 4000,
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
            time.sleep(310)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    reset_gateway()
    init_simulator()
    print(datetime.datetime.now().timestamp())
    start_simulator()
    evolve()
