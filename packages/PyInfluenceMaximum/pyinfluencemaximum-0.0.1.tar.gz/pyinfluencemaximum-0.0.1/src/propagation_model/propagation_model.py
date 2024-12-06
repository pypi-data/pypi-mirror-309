import multiprocessing
import random
import statistics

import networkx as nx


def __simulate_independent_cascade(G, seeds, R):
    num_simulate = 0

    for _ in range(R):
        activated_nodes = set(seeds)
        new_activated_nodes = set()
        current_activated_nodes = set(seeds)
        while True:
            for activated_node in current_activated_nodes:
                for neighbor_node in G.neighbors(activated_node):
                    if neighbor_node in activated_nodes:
                        continue
                    if random.random() <= G.get_edge_data(activated_node, neighbor_node)['weight']:
                        # 激活
                        activated_nodes.add(neighbor_node)
                        new_activated_nodes.add(neighbor_node)
            if len(new_activated_nodes) == 0:
                break

            current_activated_nodes = new_activated_nodes
            new_activated_nodes = set()

        num_simulate += len(activated_nodes)
    return num_simulate / R


def __simulate_linear_threshold(G, seeds, R):
    num_simulate = 0

    for _ in range(R):
        node_theta_list = [random.random() for _ in range(G.number_of_nodes())]
        activated_nodes = set(seeds)
        new_activated_nodes = set()
        activatable_nodes = set(G.nodes) - activated_nodes
        while True:
            for node in activatable_nodes:
                sum_w = sum(G.edges[pre, node]['weight'] for pre in G.predecessors(node) if pre in activated_nodes)
                if sum_w >= node_theta_list[node]:
                    activated_nodes.add(node)
                    new_activated_nodes.add(node)

            if len(new_activated_nodes) == 0:
                break

            activatable_nodes -= new_activated_nodes
            new_activated_nodes = set()

        num_simulate += len(activated_nodes)
    return num_simulate / R


def simulate_monte_carlo(G, seeds, R, propagation_model, multi_process=False, num_workers=-1):
    if propagation_model.upper() == 'IC':
        dm = __simulate_independent_cascade
    elif propagation_model.upper() == 'LT':
        dm = __simulate_linear_threshold
    else:
        raise ValueError('Unsupported activation strategy')

    if multi_process:
        with multiprocessing.Pool(num_workers) as pool:
            mc_args = [[G, seeds, int(R / num_workers)] for _ in range(num_workers)]
            results = pool.starmap(dm, mc_args)
        return statistics.mean(results)
    else:
        return dm(G, seeds, R)

