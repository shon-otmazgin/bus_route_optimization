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
    routes_df = routes_df.loc[[1, 2, 3, 4, 5, 20, 21, 38, 39, 40, 41, 56, 74, 81, 82, 87, 88, 89, 90, 91, 92, 101, 103, 105, 133, 134, 135, 136, 144, 145, 146, 147, 155, 156, 157, 158, 166, 167, 168, 169, 188, 189, 190, 191, 204, 246, 250, 254, 255, 260, 261, 262, 264, 265, 266, 267, 268, 269, 335, 336, 337, 341, 342, 343, 347, 348, 349, 350, 351, 352, 356, 357, 358, 362, 363, 364, 368, 369, 381, 382, 383, 400, 401, 414, 415, 429, 431, 433, 435, 449, 450, 463, 464, 476, 488, 489, 490, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 503]]

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

    start = 9
    end = 10
    results = []
    for k in range(start, end):
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

    for k in range(start, end):
        print(f'k={k} deadhead:{route_optimizer.get_schedule_OpEx(results[k-start][0]) / DEADHEAD}, time: {results[k-start][1]:0.2f}s')


