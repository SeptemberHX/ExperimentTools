# -*- coding: utf-8 -*-

# @Time : 2019/12/3 16:13
# @Author : SeptemberHX
# @File : physical_connection.py
# @Description:

import json

edge_id_list = [
    'aws-cluster-master',
    'aws-cluster-01',
    'aws-cluster-02',
    'aws-cluster-03',
    'aws-cluster-04',
    'aws-cluster-05',
    'aws-cluster-06',
    'aws-cluster-07',
    'aws-cluster-08',
    'aws-cluster-09',
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
                    'delay': 5,
                    'bandwidth': 1000
                }
            }
            result.append(c_info)
    for i in range(0, len(cloud_id_list)):
        for j in range(0, len(edge_id_list)):
            c_info = {
                'successor': edge_id_list[i],
                'predecessor': edge_id_list[j],
                'connection': {
                    'delay': 55,
                    'bandwidth': 200
                }
            }
            result.append(c_info)
    print(json.dumps(result, indent=4))