#!/bin/env/python3

from typing import List
import json
import random


class MPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_json(self):
        return {
            'x': self.x,
            'y': self.y
        }


class MDemand:
    def __init__(self, id, userId, functionId, slaLevel, serviceName):
        self.id = id
        self.userId = userId
        self.functionId = functionId
        self.slaLevel = slaLevel
        self.serviceName = serviceName

    def to_json(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'functionId': self.functionId,
            'slaLevel': self.slaLevel,
            'serviceId': self.serviceName
        }


class MDemandChain:
    def __init__(self):
        self.demand_list = []  # type: List[MDemand]

    def add_demand(self, demand: MDemand):
        self.demand_list.append(demand)

    def to_json(self):
        j_dict = {
            'demandIdList': [],
            'demandMap': {}
        }
        for demand in self.demand_list:
            j_dict['demandIdList'].append(demand.id)
            j_dict['demandMap'][demand.id] = demand.to_json()
        return j_dict


class MUser:
    def __init__(self, id, position: MPosition):
        self.id = id
        self.position = position
        self.demandChainList = []   # type: List[MDemandChain]

    def add_demand_chain(self, demand_chain: MDemandChain):
        self.demandChainList.append(demand_chain)

    def to_json(self):
        r_dict = {
            'demandChainList': [],
            'position': self.position.to_json(),
            'id': self.id
        }
        for demand_chain in self.demandChainList:
            r_dict['demandChainList'].append(demand_chain.to_json())
        return r_dict


def read_services_info(file_path):
    r_info_dict = {}
    with open(file_path) as f:
        info_dict_list = json.load(f)
        for info_dict in info_dict_list:
            if info_dict['serviceName'] not in r_info_dict:
                r_info_dict[info_dict['serviceName']] = []
            r_info_dict[info_dict['serviceName']].append(info_dict)
    return r_info_dict


def random_select_sla_level(service_info, service_name, function_id, r : random.Random):
    if service_name is not None:
        i = service_info[service_name][r.randint(0, len(service_info[service_name]) - 1)]
        for interface in i['interfaceMap'].values():
            if interface['functionId'] == function_id:
                return interface['slaLevel']
    else:
        sla_level_set = set()
        for service_name in service_info:
            for service in service_info[service_name]:
                for interface in service['interfaceMap'].values():
                    if interface['functionId'] == function_id:
                        sla_level_set.add(interface['slaLevel'])
        sla_level_list = list(sla_level_set)
        return sla_level_list[r.randint(0, len(sla_level_list) - 1)]


generator_random = random.Random(3000000)
# generator_random = random.Random(2000000)

def generate_canteen_demand_list(user_id, service_info):
    demand_chain = MDemandChain()

    f1 = 'canteen_function'
    r1 = generator_random.random()
    if r1 < 0.4:
        service1 = 'ali_service'
    elif r1 < 0.8:
        service1 = 'meituan_service'
    else:
        service1 = None
    d1 = MDemand(
        id='{0}_{1}_canteen'.format(user_id, f1),
        userId=user_id,
        functionId=f1,
        slaLevel=random_select_sla_level(service_info, service1, f1, generator_random),
        serviceName=service1
    )
    demand_chain.add_demand(d1)

    f1 = 'car_function'
    r1 = generator_random.random()
    if r1 < 0.4:
        service1 = 'didi_service'
    elif r1 < 0.8:
        service1 = 'taxi_service'
    else:
        service1 = None
    d1 = MDemand(
        id='{0}_{1}_canteen'.format(user_id, f1),
        userId=user_id,
        functionId=f1,
        slaLevel=random_select_sla_level(service_info, service1, f1, generator_random),
        serviceName=service1
    )
    demand_chain.add_demand(d1)

    f2 = 'pay_function'
    r2 = generator_random.random()
    if r2 < 0.3:
        service2 = 'ali_service'
    elif r2 < 0.5:
        service2 = 'wechat_service'
    elif r2 < 0.6:
        service2 = 'paypal_service'
    else:
        service2 = None
    d2 = MDemand(
        id='{0}_{1}_canteen'.format(user_id, f2),
        userId=user_id,
        functionId=f2,
        slaLevel=random_select_sla_level(service_info, service2, f2, generator_random),
        serviceName=service2
    )
    demand_chain.add_demand(d2)
    return demand_chain


def generate_market_demand_list(user_id, service_info):
    demand_chain = MDemandChain()

    f1 = 'market_function'
    r1 = generator_random.random()
    if r1 < 0.4:
        service1 = 'jindong_service'
    elif r1 < 0.7:
        service1 = 'ali_service'
    elif r1 < 0.9:
        service1 = 'amazon_service'
    else:
        service1 = None
    d1 = MDemand(
        id='{0}_{1}_market'.format(user_id, f1),
        userId=user_id,
        functionId=f1,
        slaLevel=random_select_sla_level(service_info, service1, f1, generator_random),
        serviceName=service1
    )
    demand_chain.add_demand(d1)

    f2 = 'pay_function'
    r2 = generator_random.random()
    if r2 < 0.3:
        service2 = 'ali_service'
    elif r2 < 0.5:
        service2 = 'wechat_service'
    elif r2 < 0.6:
        service2 = 'paypal_service'
    else:
        service2 = None
    d2 = MDemand(
        id='{0}_{1}_market'.format(user_id, f2),
        userId=user_id,
        functionId=f2,
        slaLevel=random_select_sla_level(service_info, service2, f2, generator_random),
        serviceName=service2
    )
    demand_chain.add_demand(d2)

    f2 = 'delivery_function'
    r2 = generator_random.random()
    if r2 < 0.3:
        service2 = 'shunfeng_service'
    elif r2 < 0.5:
        service2 = 'cainiao_service'
    elif r2 < 0.6:
        service2 = 'jindong_service'
    else:
        service2 = None
    d2 = MDemand(
        id='{0}_{1}_market'.format(user_id, f2),
        userId=user_id,
        functionId=f2,
        slaLevel=random_select_sla_level(service_info, service2, f2, generator_random),
        serviceName=service2
    )
    demand_chain.add_demand(d2)

    r2 = generator_random.random()
    if r2 < 0.6:  # whether sell the budges
        f2 = 'market_function'
        r2 = generator_random.random()
        if r2 < 0.4:
            service2 = 'jindong_service'
        elif r2 < 0.7:
            service2 = 'ali_service'
        elif r2 < 0.9:
            service2 = 'amazon_service'
        else:
            service2 = None
        d2 = MDemand(
            id='{0}_{1}_resell_market'.format(user_id, f2),
            userId=user_id,
            functionId=f2,
            slaLevel=random_select_sla_level(service_info, service2, f2, generator_random),
            serviceName=service2
        )
        demand_chain.add_demand(d2)
    return demand_chain


def generate_bike_demand_list(user_id, service_info):
    demand_chain = MDemandChain()

    f1 = 'share_bike_function'
    r1 = generator_random.random()
    if r1 < 0.4:
        service1 = 'mobi_service'
    elif r1 < 0.8:
        service1 = 'ofo_service'
    else:
        service1 = None
    d1 = MDemand(
        id='{0}_{1}_share_bike'.format(user_id, f1),
        userId=user_id,
        functionId=f1,
        slaLevel=random_select_sla_level(service_info, service1, f1, generator_random),
        serviceName=service1
    )
    demand_chain.add_demand(d1)

    f1 = 'navigation_function'
    r1 = generator_random.random()
    if r1 < 0.4:
        service1 = 'gaode_service'
    elif r1 < 0.8:
        service1 = 'baidu_service'
    else:
        service1 = None
    d1 = MDemand(
        id='{0}_{1}_share_bike'.format(user_id, f1),
        userId=user_id,
        functionId=f1,
        slaLevel=random_select_sla_level(service_info, service1, f1, generator_random),
        serviceName=service1
    )
    demand_chain.add_demand(d1)

    f2 = 'pay_function'
    r2 = generator_random.random()
    if r2 < 0.3:
        service2 = 'ali_service'
    elif r2 < 0.5:
        service2 = 'wechat_service'
    elif r2 < 0.6:
        service2 = 'paypal_service'
    else:
        service2 = None
    d2 = MDemand(
        id='{0}_{1}_share_bike'.format(user_id, f2),
        userId=user_id,
        functionId=f2,
        slaLevel=random_select_sla_level(service_info, service2, f2, generator_random),
        serviceName=service2
    )
    demand_chain.add_demand(d2)
    return demand_chain


def generate_hotel_demand_list(user_id, service_info):
    demand_chain = MDemandChain()

    f1 = 'hotel_function'
    r1 = generator_random.random()
    if r1 < 0.4:
        service1 = 'xiecheng_service'
    elif r1 < 0.8:
        service1 = 'meituan_service'
    else:
        service1 = None
    d1 = MDemand(
        id='{0}_{1}_hotel'.format(user_id, f1),
        userId=user_id,
        functionId=f1,
        slaLevel=random_select_sla_level(service_info, service1, f1, generator_random),
        serviceName=service1
    )
    demand_chain.add_demand(d1)

    r1 = generator_random.random()
    if r1 < 0.4:  # order food on the App
        f1 = 'carryout_function'
        r1 = generator_random.random()
        if r1 < 0.4:
            service1 = 'meituan_service'
        elif r1 < 0.8:
            service1 = 'eleme_service'
        else:
            service1 = None
        d1 = MDemand(
            id='{0}_{1}_hotel'.format(user_id, f1),
            userId=user_id,
            functionId=f1,
            slaLevel=random_select_sla_level(service_info, service1, f1, generator_random),
            serviceName=service1
        )
        demand_chain.add_demand(d1)

    f2 = 'pay_function'
    r2 = generator_random.random()
    if r2 < 0.3:
        service2 = 'ali_service'
    elif r2 < 0.5:
        service2 = 'wechat_service'
    elif r2 < 0.6:
        service2 = 'paypal_service'
    else:
        service2 = None
    d2 = MDemand(
        id='{0}_{1}_hotel'.format(user_id, f2),
        userId=user_id,
        functionId=f2,
        slaLevel=random_select_sla_level(service_info, service2, f2, generator_random),
        serviceName=service2
    )
    demand_chain.add_demand(d2)
    return demand_chain


def generate_game_demand_list(user_id, service_info):
    demand_chain = MDemandChain()

    # select game_service
    f1 = 'game_function'
    r1 = generator_random.random()
    if r1 < 0.4:
        service1 = 'tencent_service'
    elif r1 < 0.8:
        service1 = 'netease_service'
    else:
        service1 = None
    d1 = MDemand(
        id='{0}_{1}_game'.format(user_id, f1),
        userId=user_id,
        functionId=f1,
        slaLevel=random_select_sla_level(service_info, service1, f1, generator_random),
        serviceName=service1
    )
    demand_chain.add_demand(d1)

    r2 = generator_random.random()
    if r2 < 0.6:  # whether use chat_service
        f2 = 'chat_function'
        r2 = generator_random.random()
        if r2 < 0.4:
            service2 = 'tencent_service'
        elif r2 < 0.8:
            service2 = 'yy_service'
        else:
            service2 = None
        d2 = MDemand(
            id='{0}_{1}_game'.format(user_id, f2),
            userId=user_id,
            functionId=f2,
            slaLevel=random_select_sla_level(service_info, service2, f2, generator_random),
            serviceName=service2
        )
        demand_chain.add_demand(d2)

    r2 = generator_random.random()
    if r2 < 0.6:  # whether use chat_service
        f2 = 'stream_function'
        r2 = generator_random.random()
        if r2 < 0.4:
            service2 = 'bilibili_service'
        elif r2 < 0.8:
            service2 = 'douyu_service'
        else:
            service2 = None
        d2 = MDemand(
            id='{0}_{1}_game'.format(user_id, f2),
            userId=user_id,
            functionId=f2,
            slaLevel=random_select_sla_level(service_info, service2, f2, generator_random),
            serviceName=service2
        )
        demand_chain.add_demand(d2)

    r2 = generator_random.random()
    if r2 < 0.6:  # whether use chat_service
        f2 = 'pay_function'
        r2 = generator_random.random()
        if r2 < 0.3:
            service2 = 'ali_service'
        elif r2 < 0.5:
            service2 = 'wechat_service'
        elif r2 < 0.6:
            service2 = 'paypal_service'
        else:
            service2 = None
        d2 = MDemand(
            id='{0}_{1}_game'.format(user_id, f2),
            userId=user_id,
            functionId=f2,
            slaLevel=random_select_sla_level(service_info, service2, f2, generator_random),
            serviceName=service2
        )
        demand_chain.add_demand(d2)
    return demand_chain


def generate_demandchain_list(user_id, sercie_info):
    chain_list_prev = []
    chain_list_curr = []
    r = generator_random.random()
    d_prev = None
    if r < 0.8:
        d_prev = generate_market_demand_list(user_id, sercie_info)
        chain_list_prev.append(d_prev)
    r = generator_random.random()
    if r < 0.4:  # 40% chance not change
        if d_prev is not None:
            chain_list_curr.append(d_prev)
    elif r < 0.8:  # 40% chance change demands
        chain_list_curr.append(generate_market_demand_list(user_id, sercie_info))
    else:  # 20% chance abandon this demand
        pass

    d_prev = None
    r = generator_random.random()
    if r < 0.6:
        d_prev = generate_game_demand_list(user_id, sercie_info)
        chain_list_prev.append(d_prev)
    r = generator_random.random()
    if r < 0.4:  # 40% chance not change
        if d_prev is not None:
            chain_list_curr.append(d_prev)
    elif r < 0.8:  # 40% chance change demands
        chain_list_curr.append(generate_game_demand_list(user_id, sercie_info))
    else:  # 20% chance abandon this demand
        pass

    d_prev = None
    r = generator_random.random()
    if r < 0.6:
        d_prev = generate_bike_demand_list(user_id, sercie_info)
        chain_list_prev.append(d_prev)
    r = generator_random.random()
    if r < 0.4:  # 40% chance not change
        if d_prev is not None:
            chain_list_curr.append(d_prev)
    elif r < 0.8:  # 40% chance change demands
        chain_list_curr.append(generate_bike_demand_list(user_id, sercie_info))
    else:  # 20% chance abandon this demand
        pass

    d_prev = None
    r = generator_random.random()
    if r < 0.3:
        d_prev = generate_hotel_demand_list(user_id, sercie_info)
        chain_list_prev.append(d_prev)
    r = generator_random.random()
    if r < 0.4:  # 40% chance not change
        if d_prev is not None:
            chain_list_curr.append(d_prev)
    elif r < 0.8:  # 40% chance change demands
        chain_list_curr.append(generate_hotel_demand_list(user_id, sercie_info))
    else:  # 20% chance abandon this demand
        pass

    d_prev = None
    r = generator_random.random()
    if r < 0.5:
        d_prev = generate_canteen_demand_list(user_id, sercie_info)
        chain_list_prev.append(d_prev)
    r = generator_random.random()
    if r < 0.4:  # 40% chance not change
        if d_prev is not None:
            chain_list_curr.append(d_prev)
    elif r < 0.8:  # 40% chance change demands
        chain_list_curr.append(generate_canteen_demand_list(user_id, sercie_info))
    else:  # 20% chance abandon this demand
        pass

    return chain_list_prev, chain_list_curr


def generate_user(n, x_max, y_max, service_info):
    user_id = 'user_{0}'.format(n)
    position = MPosition(
        generator_random.random() * x_max,
        generator_random.random() * y_max
    )
    user_prev = MUser(user_id, position)
    user_curr = MUser(user_id, position)
    chain_list_prev, chain_list_curr = generate_demandchain_list(user_id, service_info)
    while len(chain_list_prev) == 0 or len(chain_list_curr) == 0:
        print('Failed to create user, retry...')
        chain_list_prev, chain_list_curr = generate_demandchain_list(user_id, service_info)
    for chain in chain_list_prev:
        user_prev.add_demand_chain(chain)
    for chain in chain_list_curr:
        user_curr.add_demand_chain(chain)
    return user_prev, user_curr


def generate_specific_user(n, x_max, y_max, service_info, common_percent):
    user_id = 'user_{0}'.format(n)
    position = MPosition(
        generator_random.random() * x_max,
        generator_random.random() * y_max
    )
    user_prev = MUser(user_id, position)
    user_curr = MUser(user_id, position)
    prev_chain = create_random_user_demand(user_id, service_info)
    if generator_random.random() < common_percent:
        next_chain = create_specific_user_demand(user_id)
    else:
        next_chain = create_random_user_demand(user_id, service_info)
    user_prev.add_demand_chain(prev_chain)
    user_curr.add_demand_chain(next_chain)
    return user_prev, user_curr


def create_simple_user():
    version = 'v1'
    for user_size in [1000]:
        print('User size: ', user_size)
        info_dict = read_services_info('/Workspace/gitlab/mdata/Lab2/TestData/{0}/{1}/service.json'.format(version, user_size))
        info_prev_list = []
        info_curr_list = []
        for i in range(0, user_size):
            print('Generate user {0}'.format(i))
            user01_prev, user01_curr = generate_user(i, 10, 10, info_dict)
            info_prev_list.append(user01_prev.to_json())
            info_curr_list.append(user01_curr.to_json())
        with open('/Workspace/gitlab/mdata/Lab2/TestData/{0}/{1}/demand_prev.json'.format(version, user_size), 'w') as f:
            json.dump(info_prev_list, f, indent=4)
        with open('/Workspace/gitlab/mdata/Lab2/TestData/{0}/{1}/demand_curr.json'.format(version, user_size), 'w') as f:
            json.dump(info_curr_list, f, indent=4)


def create_specific_user():
    version = 'common'
    user_size = 5000
    for common_percent in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]:
        print('percent: {0}'.format(common_percent))
        info_dict = read_services_info('/Workspace/gitlab/mdata/Lab2/ExperimentData/{0}/{1}/service.json'.format(version, common_percent))
        info_prev_list = []
        info_curr_list = []
        for i in range(0, user_size):
            user_prev, user_curr = generate_specific_user(i, 10, 10, info_dict, common_percent)
            info_prev_list.append(user_prev.to_json())
            info_curr_list.append(user_curr.to_json())
        with open('/Workspace/gitlab/mdata/Lab2/ExperimentData/{0}/{1}/demand_prev.json'.format(version, common_percent), 'w') as f:
            json.dump(info_prev_list, f, indent=4)
        with open('/Workspace/gitlab/mdata/Lab2/ExperimentData/{0}/{1}/demand_curr.json'.format(version, common_percent), 'w') as f:
            json.dump(info_curr_list, f, indent=4)


def create_specific_user_demand(user_id):
    demand_chain = MDemandChain()
    # select game_service
    f1 = 'game_function'
    service1 = 'tencent_service'
    d1 = MDemand(
        id='{0}_{1}_game'.format(user_id, f1),
        userId=user_id,
        functionId=f1,
        slaLevel=2,
        serviceName=service1
    )
    demand_chain.add_demand(d1)

    f2 = 'chat_function'
    service2 = 'yy_service'
    d2 = MDemand(
        id='{0}_{1}_game'.format(user_id, f2),
        userId=user_id,
        functionId=f2,
        slaLevel=1,
        serviceName=service2
    )
    demand_chain.add_demand(d2)

    f2 = 'stream_function'
    service2 = 'bilibili_service'
    d2 = MDemand(
        id='{0}_{1}_test'.format(user_id, f2),
        userId=user_id,
        functionId=f2,
        slaLevel=2,
        serviceName=service2
    )
    demand_chain.add_demand(d2)
    return demand_chain


def create_random_user_demand(user_id, result_info):
    demand_chain = MDemandChain()
    for i in range(0, 3):
        flag = True
        while flag:
            service_names = list(result_info.keys())
            service_name = service_names[generator_random.randint(0, len(service_names) - 1)]
            service_list_of_same_name = result_info[service_name]
            service = service_list_of_same_name[generator_random.randint(0, len(service_list_of_same_name) - 1)]
            interfaces = list(service['interfaceMap'].keys())
            interface = service['interfaceMap'][interfaces[generator_random.randint(0, len(interfaces) - 1)]]
            d = MDemand(
                id='{0}_{1}_{2}_test'.format(user_id, interface['functionId'], service_name),
                userId=user_id,
                functionId=interface['functionId'],
                slaLevel=interface['slaLevel'],
                serviceName=service_name
            )
            exists = False
            for j in range(0, i):
                if demand_chain.demand_list[j].serviceName == d.serviceName and demand_chain.demand_list[j].functionId == d.functionId:
                    exists = True
                    break
            if not exists:
                flag = False
        demand_chain.add_demand(d)
    return demand_chain


if __name__ == '__main__':
    # info_dict = read_services_info(
    #     '/Workspace/gitlab/mdata/Lab2/ExperimentData/{0}/{1}/service.json'.format('v1', 1000))
    # print(create_random_user_demand('user_0', info_dict).to_json())
    # print(create_specific_user_demand('user_1').to_json())
    create_specific_user()