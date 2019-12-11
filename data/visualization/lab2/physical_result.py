# -*- coding: utf-8 -*-

# @Time : 2019/12/11 14:38
# @Author : SeptemberHX
# @File : physical_result.py
# @Description: 一分钟以结束时间为标识，即 00:00:00 - 00:00:59 以 00:01:00 为标识


import json
import datetime
import os
import csv
import random
import string

# 数据文件为 ip_log.log 以及 system*.log
data_dir = 'D:\\result\\result_new'
result_dir = 'D:\\result\\csv'


def parse_system_log(log_path):
    result = {}
    with open(log_path) as f:
        for line in f.readlines():
            data_str = line[73:].replace("'", '"')
            data = json.loads(data_str)
            time_str = line[1:24]
            time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S,%f')
            time = datetime.datetime(year=time.year, month=time.month, day=time.day, hour=time.hour, minute=time.minute)
            if time not in result:
                result[time] = data
    return result


def merge_system_log(log_result_list):
    result = {}
    for log_list in log_result_list:
        for time in log_list:
            if time not in result:
                result[time] = log_list[time]
    return result


def system_log_to_demand_csv(log_result_dict, dir_path):
    time_list = sorted(log_result_dict.keys())
    with open(os.path.join(dir_path, 'total_demand.csv'), 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(['time', 'count of total demand', 'totalDemandServiceNum'])
        row = []
        for time in time_list:
            row.append([time, log_result_dict[time]['totalDemandNum'], log_result_dict[time]['totalDemandServiceNum']])
        f_csv.writerows(row)


def system_log_to_resource_csv(log_result_dict, dir_path):
    time_list = sorted(log_result_dict.keys())
    with open(os.path.join(dir_path, 'resource.csv'), 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(['time', 'average CPU assigned', 'average RAM assigned'])
        row = []
        for time in time_list:
            count = 0
            cpu_percent = 0
            ram_percent = 0
            for node_id in log_result_dict[time]['nodeCpuUsagePercentMap']:
                if node_id != 'aws-us-master':
                    count += 1
                    cpu_percent += log_result_dict[time]['nodeCpuUsagePercentMap'][node_id]
                    ram_percent += log_result_dict[time]['nodeRamUsagePercentMap'][node_id]
            cpu_percent /= count
            ram_percent /= count
            row.append([time, cpu_percent, ram_percent])
        f_csv.writerows(row)


def parse_request_log(log_path):
    result_list = []  # 存储一次完整的链式请求，计算时间是，算在请求发起阶段，如果有一个 Failed，则平均时间为 0
    thread_dict = {}
    with open(log_path) as f:
        for line in f.readlines():
            split_list = line.split()
            thread_name = split_list[6]
            if thread_name not in thread_dict:
                thread_dict[thread_name] = []
            thread_dict[thread_name].append(line[line.rfind(':') + 1:])
    for thead_name in thread_dict:
        fetch_flag = False
        tmp_result_list = []
        for result in thread_dict[thread_name]:  # type: str
            if '=' in result:
                fetch_flag = True
                tmp_result_list = []
                continue
            if '+' in result:
                fetch_flag = False
                result_list.append(tmp_result_list)
                continue
            if fetch_flag:
                split_list = result.split()
                time = datetime.datetime.fromtimestamp(float(split_list[2]))
                time = datetime.datetime(year=time.year, month=time.month, day=time.day, hour=time.hour,
                                         minute=time.minute)
                tmp_result_list.append([split_list[0], split_list[1], time])
    return result_list


def merge_request_log(log_result_list):
    result_list = []
    for log_result in log_result_list:
        result_list.extend(log_result)
    return result_list


def request_log_to_failed_csv(log_result_list, dir_path):
    failed_dict = {}
    for log_result in log_result_list:
        for request in log_result:
            if request[0] == 'Failed':
                time = request[2]
                if time not in failed_dict:
                    failed_dict[time] = 0
                failed_dict[time] += 1

    time_list = sorted(failed_dict.keys())
    for i in range(0, len(time_list)):
        if i + 1 < len(time_list):
            delta = time_list[i + 1] - time_list[i]
            if delta != datetime.timedelta(minutes=1):
                for j in range(1, delta.seconds // 60):
                    fill_time = time_list[i] + datetime.timedelta(minutes=j)
                    failed_dict[fill_time] = 0

    with open(os.path.join(dir_path, 'failed.csv'), 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(['time', 'Failed Count'])
        row = []
        for time in failed_dict:
            row.append([time, failed_dict[time]])
        f_csv.writerows(row)


def request_log_avg_response_time_csv(log_result_list, dir_path):
    response_time_dict = {}
    for log_result_list in log_result_list:
        has_failed_flag = False
        for request in log_result_list:
            if request[0] == 'Failed':
                has_failed_flag = True
                break
        if has_failed_flag:
            continue

        r_time = 0.0
        for request in log_result_list:
            r_time += float(request[0])
        time = log_result_list[0][2]
        if time not in response_time_dict:
            response_time_dict[time] = []
        response_time_dict[time].append(r_time)

    with open(os.path.join(dir_path, 'avg.csv'), 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(['time', 'Average Response Time'])
        row = []
        for time in response_time_dict:
            all_time = sum(response_time_dict[time])
            avg_time = all_time / len(response_time_dict[time])
            row.append([time, avg_time])
        f_csv.writerows(row)


def main():
    system_log_dict_list = []
    request_log_dict_list = []
    for log_file_name in os.listdir(data_dir):
        if log_file_name.startswith('system'):
            system_log_dict_list.append(parse_system_log(os.path.join(data_dir, log_file_name)))
        else:
            request_log_dict_list.append(parse_request_log(os.path.join(data_dir, log_file_name)))
    system_log_dict = merge_system_log(system_log_dict_list)
    request_log_list = merge_request_log(request_log_dict_list)

    random_dir_path = os.path.join(result_dir, ''.join(random.sample(string.ascii_letters, 8)))
    os.mkdir(random_dir_path)
    print('======>  ' + random_dir_path + '  <======')
    request_log_avg_response_time_csv(request_log_list, random_dir_path)


if __name__ == '__main__':
    main()
