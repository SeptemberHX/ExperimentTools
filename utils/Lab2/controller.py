# -*- coding: utf-8 -*-

# @Time : 2019/12/7 16:04
# @Author : SeptemberHX
# @File : controller.py
# @Description:

import sys
import requests
import datetime
import time

from utils.Lab2.system_info import start_gather_system_info

ip_list = {
    '144.34.160.60': {
        'start': 0,
        'end': 300,
        'gateway': '18.144.48.157:8081'
    },
    '144.34.214.165': {
        'start': 300,
        'end': 600,
        'gateway': '13.57.52.116:8081'
    },
    '144.34.172.167': {
        'start': 600,
        'end': 900,
        'gateway': '52.53.253.108:8081'
    },
    '104.225.148.205': {
        'start': 900,
        'end': 1200,
        'gateway': '54.183.155.224:8081'
    },
    '66.42.98.44': {
        'start': 1200,
        'end': 1500,
        'gateway': '52.53.243.84:8081'
    },
    '8.3.29.104': {
        'start': 1500,
        'end': 1800,
        'gateway': '54.215.245.83:8081'
    },
    '144.202.113.140': {
        'start': 1800,
        'end': 2100,
        'gateway': '54.67.47.114:8081'
    },
    '149.28.80.33': {
        'start': 2100,
        'end': 2400,
        'gateway': '54.215.245.26:8081'
    },
    '140.82.20.242': {
        'start': 2400,
        'end': 2700,
        'gateway': '13.57.178.208:8081'
    },
    '144.34.200.189': {
        'start': 2700,
        'end': 3000,
        'gateway': '13.57.59.140:8081'
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
            response = requests.get('http://3.136.80.127:9001/mserver/evolve?type=1')
            time.sleep(100)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    reset_gateway()
    init_simulator()
    print(datetime.datetime.now().timestamp())
    start_simulator()
    # evolve()