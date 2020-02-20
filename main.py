from route_optimization.route_optimization_handler import RouteOptimizationHandler
import pandas as pd
from route_optimization.route_utils import *
import time
import numpy as np

RESTRICTED_TIME = 8 * 60


def get_k_avg_random_schedule(k=20):
    results = []
    for i in range(k):
        s = route_optimizer.get_random_schedule()
        opex = route_optimizer.get_schedule_OpEx(schedule=s) / DEADHEAD
        results.append((s, opex))
        route_optimizer.reset_C()

    avg = 0
    for res in results:
        s, opex = res
        avg += opex
    return avg / len(results)


if __name__ == '__main__':
    routes_df = pd.read_csv('dataset/service_trips.csv', index_col=0)

    # np.random.seed(42)
    # routes_df = routes_df.sample(n=100)

    route_optimizer = RouteOptimizationHandler(routes_df=routes_df, restricted_time=RESTRICTED_TIME)
    print("Starting fit...")

    started = time.time()
    route_optimizer.fit()
    print("Fit took %0.2fs" % (time.time() - started))
    print()

    started = time.time()
    s_random = route_optimizer.get_random_schedule()
    print(s_random)
    print(f'Schedule is: {route_optimizer._valid_schedule(schedule=s_random)}')
    print('OpEx:', route_optimizer.get_schedule_OpEx(s_random))
    print('Deadheads:', route_optimizer.get_schedule_OpEx(s_random) / DEADHEAD)
    print('Num of Vehicles:', len(s_random))
    print("Random Schedule Took %0.2fs" % (time.time() - started))
    print()

    start = 10
    end = 11
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
        print("Beam search Schedule Took %0.2fs" % (time.time() - started))
        results.append((s , time.time() - started))
        print()

    for k in range(start, end):
        print(f'k={k} deadhead:{route_optimizer.get_schedule_OpEx(results[k-start][0]) / DEADHEAD}, time: {results[k-start][1]:0.2f}s')


