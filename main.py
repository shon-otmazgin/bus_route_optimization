from route_optimization.route_optimization_handler import RouteOptimizationHandler
import pandas as pd
import numpy as np
from route_optimization.route_utils import *

from route_optimization.route_utils import random_element
import cProfile
import time
RESTRICTED_TIME = 8 * 60


def get_best_s(routes_df, neighbors_matrix):
    s_final = []
    for s in partitions(neighbors_matrix.index.tolist()):
        s_sorted = []
        for v in s:
            s_sorted.append(sorted(v, key=lambda trip: routes_df.loc[trip, DEPARTURE]))
        s_final.append(s_sorted)

    s_best = None
    opex_best = routes_df.shape[0] * 2 * 15 + 1
    for s in s_final:
        valid = route_optimizer._valid_schedule(s)
        if valid:
            opex = route_optimizer.get_schedule_OpEx(s)
            if opex < opex_best:
                s_best = s
                opex_best = opex
    return s_best


def random_schedule():
    k = 20

    results = []
    for i in range(k):
        s = route_optimizer.get_random_schedule()
        opex = route_optimizer.get_schedule_OpEx(schedule=s) / 15
        results.append((s, opex))
        route_optimizer.reset_C()

    avg = 0
    for res in results:
        s, opex = res
        avg += opex
        print(s)
        print(opex)
    print('avg: ', avg / len(results))


if __name__ == '__main__':
    routes_df = pd.read_csv('dataset/service_trips.csv', index_col=0)

    np.random.seed(42)
    routes_df = routes_df.sample(n=100)

    route_optimizer = RouteOptimizationHandler(routes_df=routes_df, restricted_time=RESTRICTED_TIME)
    print("Starting fit...")
    started = time.time()
    route_optimizer.fit()
    neighbors_matrix = route_optimizer.get_neighbors_matrix()
    penalty_matrix = route_optimizer.get_penalty_matrix()

    print("Took %0.2fs" % (time.time() - started))
    print()

    s_random = route_optimizer.get_random_schedule()
    print(s_random)
    print(f'Schedule is: {route_optimizer._valid_schedule(schedule=s_random)}')
    print('OpEx:', route_optimizer.get_schedule_OpEx(s_random))
    print('Deadheads:', route_optimizer.get_schedule_OpEx(s_random) / DEADHEAD)
    print('Num of Vehicles:', len(s_random))
    print()

    results = []
    for k in range(2, 30):
        print(f'-------------k={k}-------------')
        started = time.time()
        route_optimizer.reset_C()
        s = route_optimizer.get_schedule(k=k)
        deadheads = route_optimizer.get_schedule_OpEx(s) / DEADHEAD

        print(s)
        print(f'Schedule is: {route_optimizer._valid_schedule(schedule=s)}')
        print('OpEx:', route_optimizer.get_schedule_OpEx(schedule=s))
        print('Deadheads:', deadheads)
        print('Num of Vehicles:', len(s))
        print("Took %0.2fs" % (time.time() - started))
        results.append((s , time.time() - started))
        print()

    for k in range(2, 30):
        print(f'k={k} deadhead: {route_optimizer.get_schedule_OpEx(results[k-2][0]) / DEADHEAD}, time: {results[k-2][1]:0.2f}s')


