# -*- coding: utf-8 -*-

# @Time : 2019/12/3 15:09
# @Author : SeptemberHX
# @File : requst_simulation.py
# @Description:

import datetime
import requests
import json
import time
import random
from utils.common.logger import get_logger


service_info = {}
logger = get_logger('request_simulation')


def load_service_info(service_json_path):
    global service_info
    with open(service_json_path) as f:
        service_data = json.load(f)
        for service in service_data:
            if service['serviceName'] not in service_info:
                service_info[service['serviceName']] = []
            service_info[service['serviceName']].append(service)


def get_response_and_indata_size_with_service_and_function(service_name, function_id):
    global service_info
    if service_name in service_info:
        interface_map = service_info[service_name][0]['interfaceMap']
        for interface in interface_map.values():
            if interface['functionId'] == function_id:
                return interface['patternUrl'], interface['inDataSize']
    else:
        raise Exception(service_name + ' not in the service database')
    return None


def do_request_chain(url, user_demand_list):
    i = 0
    logger.info('======')
    while i < len(user_demand_list):
        user_demand = user_demand_list[i]
        service_name = user_demand['serviceId']
        function_id = user_demand['functionId']
        _, in_data_size = get_response_and_indata_size_with_service_and_function(service_name, function_id)
        msg, response_time = do_request(url, in_data_size, user_demand)
        if msg == 'Fail':
            logger.info('Failed ' + user_demand['id'])
        else:
            for j in range(i, len(user_demand_list)):
                next_service_name = user_demand_list[j]['serviceId']
                next_function_id = user_demand_list[j]['functionId']
                next_res_msg, _ = get_response_and_indata_size_with_service_and_function(next_service_name, next_function_id)
                if next_res_msg == msg:
                    i = j
                    break
            logger.info(str(response_time) + ' ' + user_demand['id'])
        i += 1
        time.sleep(random.randint(1, 3))
    logger.info('++++++')


def do_request(url, data_size_in_kb, user_demand):
    json_data = {
        "userDemand": user_demand,
        "data": {
            "valueMap": {
                "interval": 0,
                "data": '+'*1024*data_size_in_kb
            }
        }
    }
    start_time = datetime.datetime.now().timestamp() * 1000  # mills
    r = requests.post(url, json=json_data)
    end_time = datetime.datetime.now().timestamp() * 1000
    if r.json()['status'] == 'Fail':
        interval = 0
        msg = 'Fail'
    else:
        print(r.json())
        interval = r.json()['valueMap']['interval']
        msg = r.json()['valueMap']['msg']
    response_time = end_time - start_time - interval
    return msg, response_time


def register_user(url, user_info):
    requests.post(url, json=user_info)


def convert_demandchain_to_list(demand_chain):
    result = []
    for demand_id in demand_chain['demandIdList']:
        result.append(demand_chain['demandMap'][demand_id])
    return result


def do_request_user(url, user_info):
    demand_list_list = []
    for demand_chain in user_info['demandChainList']:
        demand_list = convert_demandchain_to_list(demand_chain)
        demand_list_list.append(demand_list)
    for demand_list in demand_list_list:
        do_request_chain(url, demand_list)


def simulation_single_user(register_url, gateway_url, user_info_map: dict):
    """
    The user_info_map is passed time to user bean.
    {0: info1, 100: info2, ...} means info1 is the first info. After 100 seconds, changing to info2, etc.
    """
    time_list = sorted(user_info_map.keys())
    assert time_list[0] == 0
    i = 0
    register_user(register_url, user_info_map[0])
    start_timestamp = datetime.datetime.now().timestamp()  # seconds
    while i < len(time_list):
        do_request_user(gateway_url, user_info_map[time_list[i]])
        time.sleep(random.randint(0, 3))
        curr_timestamp = datetime.datetime.now().timestamp()
        if i + 1 < len(time_list) and curr_timestamp - start_timestamp > time_list[i + 1]:
            i += 1
            register_user(register_url, user_info_map[time_list[i]])
