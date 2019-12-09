# -*- coding: utf-8 -*-

# @Time : 2019/12/6 20:37
# @Author : SeptemberHX
# @File : main.py
# @Description:

import threading
import os
import json

from utils.Lab2.requst_simulation import simulation_single_user, load_service_info
from flask import Flask, request

app = Flask(__name__)
target_user_info = {}
gateway_ip_port = None


def load_user_info_from_dict(dict_path):
    user_info = {}
    for time_gap in os.listdir(dict_path):
        with open(os.path.join(dict_path, time_gap, 'demands.json')) as f:
            demand_json = json.load(f)
            user_info[time_gap] = demand_json
    return user_info


def fetch_target_user_list(user_info, start_index, end_index):
    result_info = {}
    for time_gap in user_info:
        for user in user_info[time_gap]:
            user_id = user['id']  # type: str
            id_int = int(user_id.split('_')[-1])
            if id_int < start_index or id_int >= end_index:
                break
            if user_id not in result_info:
                result_info[user_id] = {}
            result_info[user_id][int(time_gap)] = user
    return result_info


@app.route('/load', methods=['POST'])
def load_data():
    global target_user_info
    global gateway_ip_port
    data_json = json.loads(request.get_data())
    gateway_ip_port = data_json['gateway']
    user_info = load_user_info_from_dict('./lab_data')
    target_user_info = fetch_target_user_list(user_info, data_json['start'], data_json['end'])
    load_service_info('./service.json')
    return ''


@app.route('/start', methods=['GET'])
def start_simulation():
    global target_user_info
    global gateway_ip_port
    for user_id in target_user_info.keys():
        threading.Thread(target=simulation_single_user, kwargs={
            'register_url': 'http://{0}/register'.format(gateway_ip_port),
            'gateway_url': 'http://{0}/request'.format(gateway_ip_port),
            'user_info_map': target_user_info[user_id]
        }).start()
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=54321)
    # user_info = load_user_info_from_dict('./lab_data')
    # target_user_info = fetch_target_user_list(user_info, 0, 300)
    # print(target_user_info['user_0'])
