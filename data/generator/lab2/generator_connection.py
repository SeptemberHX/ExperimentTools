import random
import json

if __name__ == '__main__':
    node_id_list = []
    c_info_list = []
    delay_list = [10, 15, 20, 25]
    bandwidth_list = [100, 150, 120]
    for i in range(1, 11):
        node_id_list.append('node{0}'.format(i))
    for i in range(0, 10):
        for j in range(i + 1, 10):
            c_info = {
                'successor': node_id_list[i],
                'predecessor': node_id_list[j],
                'connection': {
                    'delay': delay_list[random.randint(0, 3)],
                    'bandwidth': bandwidth_list[random.randint(0, 2)]
                }
            }
            c_info_list.append(c_info)
    for i in range(1, 5):
        c_info = {
            'successor': node_id_list[i],
            'predecessor': 'node11',
            'connection': {
                'delay': delay_list[random.randint(0, 3)] * 2,
                'bandwidth': bandwidth_list[random.randint(0, 2)]
            }
        }
        c_info_list.append(c_info)
    for i in range(5, 10):
        c_info = {
            'successor': node_id_list[i],
            'predecessor': 'node11',
            'connection': {
                'delay': delay_list[random.randint(0, 3)] * 4,
                'bandwidth': bandwidth_list[random.randint(0, 2)]
            }
        }
        c_info_list.append(c_info)

    for i in range(1, 5):
        c_info = {
            'successor': node_id_list[i],
            'predecessor': 'node12',
            'connection': {
                'delay': delay_list[random.randint(0, 3)] * 4,
                'bandwidth': bandwidth_list[random.randint(0, 2)]
            }
        }
        c_info_list.append(c_info)
    for i in range(5, 10):
        c_info = {
            'successor': node_id_list[i],
            'predecessor': 'node12',
            'connection': {
                'delay': delay_list[random.randint(0, 3)] * 2,
                'bandwidth': bandwidth_list[random.randint(0, 2)]
            }
        }
        c_info_list.append(c_info)
    print(json.dumps(c_info_list, indent=4))