import queue
import random
from collections import Counter
from itertools import chain

import networkx as nx
import numpy as np
from tqdm import tqdm
from networkx import DiGraph

from propagation_model import simulate_monte_carlo


def greedy(G: DiGraph, k: int, propagation_model: str, R: int, return_spread=False, show_bar=True, multi_process=False,
           num_workers=-1):
    seeds = []  # 种子集
    max_num_propagation_nodes = 0
    max_node = None
    spread = []
    if show_bar:
        with tqdm(total=k, desc=f'R: {R}') as tbar:
            for _ in range(k):
                for node in G.nodes:
                    if node in seeds:
                        continue
                    now_num_propagation_nodes = simulate_monte_carlo(G, seeds + [node], R, propagation_model,
                                                                     multi_process, num_workers)
                    if now_num_propagation_nodes > max_num_propagation_nodes:
                        max_num_propagation_nodes = now_num_propagation_nodes
                        max_node = node
                spread.append(max_num_propagation_nodes)
                seeds.append(max_node)
                tbar.update(1)
    else:
        for _ in range(k):
            for node in G.nodes:
                if node in seeds:
                    continue
                now_num_propagation_nodes = simulate_monte_carlo(G, seeds + [node], R, propagation_model, True, 5)
                if now_num_propagation_nodes > max_num_propagation_nodes:
                    max_num_propagation_nodes = now_num_propagation_nodes
                    max_node = node
                    spread.append(max_num_propagation_nodes)
            seeds.append(max_node)

    if return_spread:
        return seeds, spread

    return seeds


class Node:
    def __init__(self, mg, i, node):
        self.mg = mg
        self.i = i
        self.node = node

    def __lt__(self, other):
        return -self.mg < -other.mg

    def __str__(self) -> str:
        return f'mg: {self.mg}, i: {self.i}, node: {self.node}'


def lazy_greedy(G: DiGraph, k: int, propagation_model: str, R: int, return_spread=False, show_bar=True,
                multi_process=False, num_workers=-1):
    seeds = []  # 种子集
    max_num_propagation_nodes = 0
    spread = []

    iteration = 0
    Q = queue.PriorityQueue()

    if show_bar:
        with tqdm(total=k + len(G.nodes()), desc=f'R: {R}') as tbar:
            for node in G.nodes():
                mg = simulate_monte_carlo(G, seeds + [node], R, propagation_model, multi_process, num_workers)
                node_class = Node(mg, iteration, node)
                Q.put(node_class)
                tbar.set_postfix({'margin gain': mg})
                tbar.update(1)

            while k > iteration:
                # 取出最大mg的节点
                u = Q.get()
                if u.i == iteration:
                    seeds.append(u.node)
                    iteration += 1
                    max_num_propagation_nodes += u.mg
                    spread.append(max_num_propagation_nodes)
                    tbar.set_postfix({'k': iteration, 'num_propagation': max_num_propagation_nodes})
                    tbar.update(1)
                else:
                    # 计算边际增益
                    mg = simulate_monte_carlo(G, seeds + [node], R, propagation_model, True, 5)
                    u.mg = mg - max_num_propagation_nodes if mg - max_num_propagation_nodes > 0 else 0
                    u.i = iteration
                    Q.put(u)
    else:
        for node in G.nodes():
            mg = simulate_monte_carlo(G, seeds + [node], R, propagation_model, True, 5)
            node_class = Node(mg, iteration, node)
            Q.put(node_class)

        while k > iteration:
            # 取出最大mg的节点
            u = Q.get()
            if u.i == iteration:
                seeds.append(u.node)
                iteration += 1
                max_num_propagation_nodes += u.mg
                spread.append(max_num_propagation_nodes)
            else:
                # 计算边际增益
                mg = simulate_monte_carlo(G, seeds + [node], R, propagation_model, True, 5)
                u.mg = mg - max_num_propagation_nodes if mg - max_num_propagation_nodes > 0 else 0
                u.i = iteration
                Q.put(u)

    if return_spread:
        return seeds, spread

    return seeds


def __sample_subgraph_by_edge_weight(G):
    remove_edges = []
    for u, v, a in G.edges(data=True):
        if random.random() <= 1 - a['weight']:
            remove_edges.append((u, v))
    G.remove_edges_from(remove_edges)
    return G


def get_rrs(G, v):
    # 执行图采样
    G = __sample_subgraph_by_edge_weight(G.copy())
    # 计算RRS
    rrs = set()
    start_node_set = {v}
    new_node_set = set()
    while start_node_set:
        for node in start_node_set:
            rrs.update(G.predecessors(node))
            new_node_set.update(G.predecessors(node))
        start_node_set = new_node_set - rrs
        new_node_set = set()

    return rrs


def get_rrs_big_graph(G, v):
    df = nx.to_pandas_edgelist(G)
    df_sub = df[np.random.random(df.shape[0]) <= 1 - df['weight']]
    # 计算RRS
    rrs = set()
    start_node_set = {v}
    while start_node_set:
        predecessors = df_sub[df_sub['source'].isin(start_node_set)]['target'].tolist()
        rrs.update(predecessors)
        start_node_set = set(predecessors) - rrs

    return rrs


def ris(G: DiGraph, k: int, R: int, is_big=False):
    if is_big:
        gr = get_rrs_big_graph
    else:
        gr = get_rrs
    rrs = [gr(G, random.choice(list(G.nodes))) for _ in range(R)]

    seeds = []
    for _ in range(k):
        flat = chain.from_iterable(rrs)
        seed = Counter(flat).most_common(1)[0][0]
        seeds.append(seed)
        rrs = [rr for rr in rrs if seed not in rr]

    return seeds
