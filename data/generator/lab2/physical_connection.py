# -*- coding: utf-8 -*-

# @Time : 2019/12/3 16:13
# @Author : SeptemberHX
# @File : physical_connection.py
# @Description:

import json

edge_id_list = [
    'edge-master',
    'bandwagon-los-01',
    'bandwagon-los-02',
    'bandwagon-los-03',
    'bandwagon-los-04',
    'vultr-los-01',
    'vultr-los-02',
    'vultr-los-03',
    'vultr-los-04',
    'vultr-los-05'
]

cloud_id_list = [
    'aws-us-master'
]

if __name__ == '__main__':
    result = []
    for i in range(0, len(edge_id_list)):
        for j in range(i + 1, len(edge_id_list)):
            c_info = {
                'successor': edge_id_list[i],
                'predecessor': edge_id_list[j],
                'connection': {
                    'delay': 1,
                    'bandwidth': 100
                }
            }
            result.append(c_info)
    for i in range(0, len(cloud_id_list)):
        for j in range(0, len(edge_id_list)):
            c_info = {
                'successor': edge_id_list[i],
                'predecessor': edge_id_list[j],
                'connection': {
                    'delay': 1,
                    'bandwidth': 20
                }
            }
            result.append(c_info)
    print(json.dumps(result, indent=4))