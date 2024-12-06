import random
from typing import Union

from networkx import Graph, DiGraph


def set_edge_weight(G: DiGraph, edge_weight_model: str, constant_weight: float = None):
    """
    为图G中的边设置权重。

    参数:
        G (networkx.DiGraph): 一个有向图。

        edge_weight_model (str): 权重模型，可以是'CONSTANT'（常量权重），'TV'（随机选择权重），或'WC'（基于目标节点入度的倒数）。

        constant_weight (float, optional): 当edge_weight_model为'CONSTANT'时使用的常量权重。默认为None。

    抛出:
        ValueError: 如果G不是有向图，或者edge_weight_model不支持，或者当edge_weight_model为'CONSTANT'时未提供constant_weight。
    """
    # 检查图G是否为有向图
    if not G.is_directed():
        raise ValueError('G must be a directed graph')

    # 将edge_weight_model转换为大写，以便进行比较
    edge_weight_model = edge_weight_model.upper()

    # 根据不同的权重模型设置权重
    if edge_weight_model == 'CONSTANT':
        # 如果模型是'CONSTANT'且未提供constant_weight，则抛出错误
        if constant_weight is None:
            raise ValueError('Constant weight must be provided when using CONSTANT model')
        # 为每条边设置常量权重
        for u, v, a in G.edges(data=True):
            a['weight'] = constant_weight
    elif edge_weight_model == 'TV':
        # 定义权重列表，用于随机选择
        weight_list = [0.001, 0.01, 0.1]
        # 为每条边随机选择一个权重
        for u, v, a in G.edges(data=True):
            a['weight'] = random.choice(weight_list)
    elif edge_weight_model == 'WC':
        # 为每条边设置基于目标节点入度的倒数作为权重
        for u, v, a in G.edges(data=True):
            a['weight'] = 1 / G.in_degree(v)
    else:
        # 如果edge_weight_model不是上述任何一种，则抛出错误
        raise ValueError('Unsupported edge weight model')


def infection_threshold(G: Union[Graph, DiGraph]):
    """
    计算基于图G的度分布的感染阈值。

    参数:
        G (networkx.Graph): 一个无向图或有向图（注意：此函数没有使用图的方向性）。

    返回:
        float: 感染阈值。

    说明:
        该函数首先计算图中所有节点的度之和（k），然后计算所有节点度的平方和（k2）。
        感染阈值计算公式为 k / (k2 - k)，其中k2是度的平方和，k是度的总和。
        这个阈值在某些流行病学模型（如SIR模型）中用于预测疾病传播的临界条件。
    """
    # 计算图中所有节点的度之和
    k = sum(dict(G.degree()).values())

    # 计算图中所有节点度的平方和
    # 使用map函数和lambda表达式将每个度值平方，然后求和
    k2 = sum(map(lambda x: x ** 2, dict(G.degree()).values()))

    # 计算并返回感染阈值
    # 注意：这里的公式假设了节点之间的连接是随机的，并且没有考虑图的方向性（如果G是有向图）。
    # 在实际应用中，感染阈值的计算可能更加复杂，并且需要考虑更多的因素。
    return k / (k2 - k)


def topk(res_dict: dict, k: int, largest=True):
    """
    从字典中返回具有最大（或最小）k个值的键的列表。

    参数:
        res_dict (dict): 输入的字典，其值用于比较以决定键的排序。

        k (int): 要返回的键的数量。

        largest (bool): 如果为True，则返回具有最大值的k个键；如果为False，则返回具有最小值的k个键。

    返回:
        list: 一个包含k个键的列表，这些键对应于字典中最大（或最小）的值。
    """
    # 使用sorted函数对res_dict的键进行排序
    # key=lambda x: res_dict[x] 指定了排序的依据是字典中对应的值
    # reverse=largest 控制了排序的顺序：largest为True时降序，为False时升序
    sorted_keys = sorted(res_dict.keys(), key=lambda x: res_dict[x], reverse=largest)

    # 通过切片操作[:k]返回前k个排序后的键
    # 这将给出具有最大（或最小）k个值的键的列表
    return sorted_keys[:k]
