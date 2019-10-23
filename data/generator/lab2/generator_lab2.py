#!/bin/env/python3

from typing import List
import json


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
    def __init__(self, id, userId, functionId, slaLevel):
        self.id = id
        self.userId = userId
        self.functionId = functionId
        self.slaLevel = slaLevel

    def to_json(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'functionId': self.functionId,
            'slaLevel': self.slaLevel
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

    def add_demand_chain(self, demand_chain):
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


if __name__ == '__main__':
    user_id = 'user1'
    function_id = 'function1'
    slaLevel = 1
    demand_id = '{0}-{1}'.format(user_id, function_id)

    demand = MDemand(demand_id, user_id, function_id, slaLevel)
    demand_chain = MDemandChain()
    demand_chain.add_demand(demand)

    user = MUser(user_id, MPosition(1, 1))
    user.add_demand_chain(demand_chain)
    print(json.dumps(user.to_json()))