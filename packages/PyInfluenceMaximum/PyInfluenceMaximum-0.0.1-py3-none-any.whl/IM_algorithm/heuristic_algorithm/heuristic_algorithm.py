import networkx as nx
from networkx import Graph, DiGraph

from utils import set_edge_weight, topk


def degree(G: DiGraph, k: int):
    degree_dict = dict(G.out_degree())
    topk_degree = topk(degree_dict, k)
    return topk_degree


def degree_discount(G: DiGraph, k: int):
    degree = dict(G.out_degree())
    discount_degree = degree.copy()
    tv = [0] * len(G)
    seeds = []

    for _ in range(k):
        u = max(discount_degree.items(), key=lambda x: x[1])[0]
        seeds.append(u)
        discount_degree[u] = -float('inf')
        for v in G.neighbors(u):
            if v in seeds:
                continue
            tv[v] += 1
            discount_degree[v] = degree[v] - 2 * tv[v] - (degree[v] - tv[v]) * tv[v] * G.edges[u, v]['weight']

    return seeds


def page_rank(G: DiGraph, k: int):
    pr = nx.pagerank(G)
    topk_pr = topk(pr, k)
    return topk_pr


def __cores(G: DiGraph):
    """
    计算图G的k-核分解，并返回每个节点的度数。

    参数:
    G (networkx.Graph): 输入的图

    返回:
    dict: 每个节点的度数字典
    """
    nodes = list(G.nodes())  # 获取图的所有节点列表
    # 获取每个节点的度数，衡量的属性，可以修改，后续操作在此基础上修改，最终返回的也是该变量
    degree = dict(G.degree())

    # 找到最大的度数md
    md = max(degree.values())

    # 初始化bins列表，用于记录每个度数对应的起始位置
    bins = [0] * (md + 1)

    # 设置bins中每个索引对应的度数出现的个数
    for node in nodes:
        bins[degree[node]] += 1

        # 更新bins列表，为每个度数设置起始位置
    start = 1
    for d in range(md + 1):
        num = bins[d]  # 当前度数的节点数
        bins[d] = start  # 设置当前度数的起始位置
        start += num  # 更新下一个度数的起始位置

    # 初始化pos和vert字典，分别用于记录节点位置和节点与位置的映射
    pos = {node: -1 for node in nodes}  # 初始化所有节点的位置为-1
    vert = {p: -1 for p in range(1, len(nodes) + 1)}  # 初始化位置与节点的映射为-1

    # 更新节点位置pos，并设置vert映射
    for node in nodes:
        pos[node] = bins[degree[node]]  # 设置节点的位置
        vert[pos[node]] = node  # 设置位置到节点的映射
        bins[degree[node]] += 1  # 更新下一个同度数节点的位置

    # 恢复bins列表，为接下来的k-核分解做准备
    for d in range(md, 0, -1):
        bins[d] = bins[d - 1]
    bins[0] = 1  # 0度节点的起始位置总是1

    # 计算每个节点的邻居
    nbrs = {v: list(nx.all_neighbors(G, v)) for v in G}

    # k-核分解过程
    for v in vert.values():  # 遍历所有节点
        for u in nbrs[v]:  # 遍历节点v的所有邻居
            if degree[u] > degree[v]:  # 如果邻居u的度数大于v的度数
                du = degree[u]  # 邻居u的度数
                pu = pos[u]  # 邻居u的位置
                pw = bins[du]  # 邻居u的下一个位置
                w = vert[pw]  # 邻居u的下一个位置对应的节点

                # 如果u不是下一个位置的节点，则交换u和w的位置
                if u != w:
                    pos[u] = pw
                    vert[pu] = w
                    pos[w] = pu
                    vert[pw] = u

                    # 更新bins和度数
                bins[du] += 1
                degree[u] -= 1

    return degree  # 返回更新后的度数字典


def k_shell(G: DiGraph, k: int):
    ks = __cores(G)
    topk_ks = topk(ks, k)
    return topk_ks


def __current_mixed_degree(G1, G2, labda=0.7):
    """
    计算当前图G2中的点的混合度
    G1是移除节点前的图，G2是移除节点后的图
    """
    mix_degree = []
    for node in G2.nodes:
        kr = G2.degree(node)
        ki = G1.degree(node) - kr
        km = kr + labda * ki
        mix_degree.append((node, km))
    return mix_degree


def mixed_degree_decomposition(G: DiGraph, k: int = None, labda=0.7):
    """
    返回图G中每个节点的混合度
    """
    G1 = G.copy()
    mixed_degree_dict = {}
    d = 1  # 当前寻找的节点的混合度为d
    while True:
        d_nodes = [n for n, md in __current_mixed_degree(G, G1, labda) if md <= d]  # 获取所有混合度小于等于d的节点

        while len(d_nodes):
            for dn in d_nodes:
                mixed_degree_dict[dn] = d
            G1.remove_nodes_from(d_nodes)
            d_nodes = [n for n, md in __current_mixed_degree(G, G1, labda) if md <= d]
        if G1.number_of_nodes() == 0:
            break
        d = min(__current_mixed_degree(G, G1, labda), key=lambda x: x[1])[1]

    if k is None:
        return mixed_degree_dict
    else:
        topk_mixed_degree = topk(mixed_degree_dict, k)
        return topk_mixed_degree


if __name__ == '__main__':
    G = nx.erdos_renyi_graph(20, 0.1, directed=True)
    set_edge_weight(G, 'wc')
    print(G)
    print(degree(G, 10))
    print(degree_discount(G, 10))
    print(page_rank(G, 10))
    print(k_shell(G, 10))
    print(mixed_degree_decomposition(G, 10, 0.7))
