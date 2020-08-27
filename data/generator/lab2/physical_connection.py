# -*- coding: utf-8 -*-

# @Time : 2019/12/3 16:13
# @Author : SeptemberHX
# @File : physical_connection.py
# @Description:

import json

edge_id_list = [
    'edge-0',
    'edge-1',
    'edge-2',
    'edge-3',
    'edge-4',
    'edge-5',
    'edge-6',
    'edge-7',
    'edge-8',
    'edge-9',
]

cloud_id_list = [
    'cloud'
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
                'successor': cloud_id_list[i],
                'predecessor': edge_id_list[j],
                'connection': {
                    'delay': 55,
                    'bandwidth': 200
                }
            }
            result.append(c_info)
    print(json.dumps(result, indent=4))