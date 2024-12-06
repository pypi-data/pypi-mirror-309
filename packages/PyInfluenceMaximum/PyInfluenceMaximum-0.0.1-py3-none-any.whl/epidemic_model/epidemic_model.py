import multiprocessing
import random
import statistics

import utils


def __si(G, init_infectors, beta, R):
    num_infectors = 0
    for _ in range(R):
        infestors = set(init_infectors)
        new_infestors = set()
        while len(infestors) < G.number_of_nodes():
            # 传染
            for infector in infestors:
                neighbors = G.neighbors(infector)
                for neighbor in neighbors:
                    if neighbor in infestors:
                        continue
                    if random.random() <= beta:
                        new_infestors.add(neighbor)

            infestors |= new_infestors
            new_infestors = set()

        num_infectors += len(infestors)
    return num_infectors / R


def __sir(G, init_infectors, beta, gamma, R):
    num_recovered = 0

    for _ in range(R):
        infectors = set(init_infectors)
        susceptible = set(G.nodes) - infectors
        recovers = set()

        while len(infectors) > 0:
            new_infectors = set()
            for infector in list(infectors):  # 使用list以避免在迭代时修改集合
                neighbors = G.neighbors(infector)
                for neighbor in neighbors:
                    if neighbor in susceptible and random.random() <= beta:
                        new_infectors.add(neighbor)
                        susceptible.remove(neighbor)

                if random.random() <= gamma:
                    recovers.add(infector)
                    infectors.remove(infector)  # 移除已恢复的感染者

            infectors |= new_infectors  # 添加新感染者到当前感染者集合中

        num_recovered += len(recovers)

    return num_recovered / R  # 返回平均每轮恢复的人数


def simulate_epidemic_monte_carlo(G, seeds, R, stype, beta=None, gamma=None, multi_process=False, num_workers=-1):
    if stype.upper() == 'SI':
        dm = __si
    elif stype.upper() == 'SIR':
        if gamma is None:
            raise ValueError('gamma must be provided for SIR model')
        dm = __sir
    else:
        raise ValueError('Unsupported activation strategy')

    if beta is None:
        beta = utils.infection_threshold(G)

    if multi_process:
        with multiprocessing.Pool(num_workers) as pool:
            if stype.upper() == 'SI':
                mc_args = [[G, seeds, beta, int(R / num_workers)] for _ in range(num_workers)]
            elif stype.upper() == 'SIR':
                mc_args = [[G, seeds, beta, gamma, int(R / num_workers)] for _ in range(num_workers)]
            results = pool.starmap(dm, mc_args)
        return statistics.mean(results)
    else:
        if stype.upper() == 'SI':
            return dm(G, seeds, beta, R)
        elif stype.upper() == 'SIR':
            return dm(G, seeds, beta, gamma, R)
