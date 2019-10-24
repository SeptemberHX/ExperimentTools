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
        return i['interfaceMap']['{0}__{1}'.format(service_name, function_id)]['slaLevel']
    else:
        sla_level_set = set()
        for service_name in service_info:
            for service in service_info[service_name]:
                for interface in service['interfaceMap'].values():
                    if interface['functionId'] == function_id:
                        sla_level_set.add(interface['slaLevel'])
        sla_level_list = list(sla_level_set)
        return sla_level_list[r.randint(0, len(sla_level_list) - 1)]


generator_random = random.Random(1000000)


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
            id='{0}_{1}_market'.format(user_id, f2),
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
    chain_list = []
    r = generator_random.random()
    if r < 0.8:
        chain_list.append(generate_market_demand_list(user_id, sercie_info))

    r = generator_random.random()
    if r < 0.6:
        chain_list.append(generate_game_demand_list(user_id, sercie_info))

    r = generator_random.random()
    if r < 0.6:
        chain_list.append(generate_bike_demand_list(user_id, sercie_info))

    r = generator_random.random()
    if r < 0.3:
        chain_list.append(generate_hotel_demand_list(user_id, sercie_info))

    r = generator_random.random()
    if r < 0.5:
        chain_list.append(generate_canteen_demand_list(user_id, sercie_info))
    return chain_list


def generate_user(n, x_max, y_max, service_info):
    user_id = 'user_{0}'.format(n)
    position = MPosition(
        generator_random.random() * x_max,
        generator_random.random() * y_max
    )
    user = MUser(user_id, position)
    chain_list = generate_demandchain_list(user_id, service_info)
    while len(chain_list) == 0:
        chain_list = generate_demandchain_list(user_id, service_info)
    for chain in chain_list:
        user.add_demand_chain(chain)
    return user


if __name__ == '__main__':
    info_dict = read_services_info('/Workspace/gitlab/mdata/Lab2/ExperimentData/service.json')

    for i in range(0, 10000):
        user01 = generate_user(i, 10, 10, info_dict)
        print(json.dumps(user01.to_json(), indent=4))