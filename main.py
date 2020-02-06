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

    # np.random.seed(42)
    # routes_df = routes_df.sample(n=100)
    # routes_df = routes_df.loc[:100]
    # routes_df = routes_df.loc[[449, 21, 437, 317, 238, 153, 475]]
    # routes_df = routes_df.loc[[487, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 332, 333, 259]]

    # routes_df = routes_df.loc[[1, 2, 3, 4, 5]]
    # routes_df.loc[6, ORIGIN] = 1
    # routes_df.loc[6, DESTINATION] = 1
    # routes_df.loc[6, DEPARTURE] = 105
    # routes_df.loc[6, ARRIVAL] = 110

    # routes_df.loc[5, ORIGIN] = 1
    # routes_df.loc[5, DESTINATION] = 2
    # routes_df.loc[5, DEPARTURE] = 100
    # routes_df.loc[5, ARRIVAL] = 200
    #
    # routes_df.loc[4, ORIGIN] = 5
    # routes_df.loc[4, DESTINATION] = 1
    # routes_df.loc[4, DEPARTURE] = 70
    # routes_df.loc[4, ARRIVAL] = 80
    #
    # routes_df.loc[3, ORIGIN] = 1
    # routes_df.loc[3, DESTINATION] = 1
    # routes_df.loc[3, DEPARTURE] = 60
    # routes_df.loc[3, ARRIVAL] = 70
    #
    # routes_df.loc[2, ORIGIN] = 1
    # routes_df.loc[2, DESTINATION] = 1
    # routes_df.loc[2, DEPARTURE] = 40
    # routes_df.loc[2, ARRIVAL] = 50
    #
    # routes_df.loc[1, ORIGIN] = 2
    # routes_df.loc[1, DESTINATION] = 4
    # routes_df.loc[1, DEPARTURE] = 50
    # routes_df.loc[1, ARRIVAL] = 55
    # print(routes_df)

    route_optimizer = RouteOptimizationHandler(routes_df=routes_df, restricted_time=RESTRICTED_TIME)
    print("Starting fit...")
    started = time.time();
    route_optimizer.fit()
    neighbors_matrix = route_optimizer.get_neighbors_matrix()

    print("Took %0.2fs" % (time.time() - started))
    print()
    s_random = route_optimizer.get_random_schedule()
    print(s_random)
    print(f'Schedule is: {route_optimizer._valid_schedule(schedule=s_random)}')
    print('OpEx:', route_optimizer.get_schedule_OpEx(s_random))
    print('Deadheads:', route_optimizer.get_schedule_OpEx(s_random)/15)
    print('Num of Vehicles:', len(s_random))
    print()

    started = time.time()
    route_optimizer.reset_C()
    s = route_optimizer.get_schedule()
    print(s)
    print(f'Schedule is: {route_optimizer._valid_schedule(schedule=s)}')
    print('OpEx:', route_optimizer.get_schedule_OpEx(s))
    deadheads = route_optimizer.get_schedule_OpEx(s) / 15
    vehicles = len(s)
    print('Deadheads:', deadheads)
    print('Num of Vehicles:', vehicles)
    print("Took %0.2fs" % (time.time() - started))
    print()
    print(routes_df.index.to_list())
    # best_s = get_best_s(routes_df=routes_df, neighbors_matrix=neighbors_matrix)
    # print(f'best s {best_s}')
    # print(f'opex {route_optimizer.get_schedule_OpEx(best_s) / 15}')