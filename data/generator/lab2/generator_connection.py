import random
import json

if __name__ == '__main__':
    node_id_list = []
    c_info_list = []
    bandwidth_list = [100, 150, 120]
    for i in range(1, 21):
        node_id_list.append('node{0}'.format(i))
    for i in range(0, 20):
        for j in range(i + 1, 20):
            c_info = {
                'successor': node_id_list[i],
                'predecessor': node_id_list[j],
                'connection': {
                    'delay': random.randint(1, 10),
                    'bandwidth': bandwidth_list[random.randint(0, 2)]
                }
            }
            c_info_list.append(c_info)
    for i in range(0, 10):
        c_info = {
            'successor': node_id_list[i],
            'predecessor': 'node21',
            'connection': {
                'delay': random.randint(60, 80),
                'bandwidth': bandwidth_list[random.randint(0, 2)]
            }
        }
        c_info_list.append(c_info)
    for i in range(10, 20):
        c_info = {
            'successor': node_id_list[i],
            'predecessor': 'node21',
            'connection': {
                'delay': random.randint(100, 120),
                'bandwidth': bandwidth_list[random.randint(0, 2)]
            }
        }
        c_info_list.append(c_info)

    for i in range(0, 10):
        c_info = {
            'successor': node_id_list[i],
            'predecessor': 'node22',
            'connection': {
                'delay': random.randint(100, 120),
                'bandwidth': bandwidth_list[random.randint(0, 2)]
            }
        }
        c_info_list.append(c_info)
    for i in range(10, 20):
        c_info = {
            'successor': node_id_list[i],
            'predecessor': 'node22',
            'connection': {
                'delay': random.randint(60, 80),
                'bandwidth': bandwidth_list[random.randint(0, 2)]
            }
        }
        c_info_list.append(c_info)
    print(json.dumps(c_info_list, indent=4))