import logging

import pandas as pd
import numpy as np
import random
import math

from route_optimization.route_utils import *


class RouteOptimizationHandler:
    logger = logging.getLogger('RouteOptimizationHandler')
    logging.basicConfig(format=FORMAT)

    def __init__(self, routes_df: pd.DataFrame, restricted_time: int):
        self.routes_df = routes_df
        self.restricted_time = restricted_time
        self.N = set(self.routes_df.index)

    def get_deadhead(self, id_1: int, id_2: int) -> int:
        return 15 if self.routes_df.loc[id_1][DESTINATION] != self.routes_df.loc[id_2][ORIGIN] else 0

    def valid_pair(self, id_1: int, id_2: int) -> bool:
        return True \
            if self.routes_df.loc[id_1][ARRIVAL] + self.get_deadhead(id_1, id_2) <= self.routes_df.loc[id_2][DEPARTURE] \
            else False

    def valid_vehicle(self, vehicle: list) -> bool:
        for trip_1, trip_2 in pairwise(vehicle):
            if not self.valid_pair(id_1=trip_1, id_2=trip_2):
                return False
        return True if vehicle else False

    def deadhead_duration(self, vehicle: list) -> int:
        if not self.valid_vehicle(vehicle=vehicle):
            raise InvalidVehicleError(f'Vehicle {vehicle} is invalid')
        duration = DEADHEAD*2
        for trip_1, trip_2 in pairwise(vehicle):
            duration += self.get_deadhead(id_1=trip_1, id_2=trip_2)
        return duration

    def restricted_vehicle(self, vehicle: list) -> bool:
        if not self.valid_vehicle(vehicle=vehicle):
            return False
        duration = self.deadhead_duration(vehicle=vehicle)
        for trip in vehicle:
            duration += self.routes_df.loc[trip][ARRIVAL] - self.routes_df.loc[trip][DEPARTURE]
        return True if duration <= self.restricted_time else False

    def valid_schedule(self, schedule: list) -> bool:
        for vehicle in schedule:
            if not self.restricted_vehicle(vehicle):
                return False
        return True

    def get_schedule_OpEx(self, schedule: list) -> int:
        if not self.valid_schedule(schedule=schedule):
            raise InvalidScheduleError(f'Schedule {schedule} is invalid')
        return sum([self.deadhead_duration(vehicle) for vehicle in schedule])

    def get_N(self):
        return self.N

    def get_matrices(self):
        neighbors_matrix = pd.DataFrame(False, index=self.routes_df.index, columns=self.routes_df.index)
        penalty_matrix = pd.DataFrame(np.nan, index=self.routes_df.index, columns=self.routes_df.index)

        u_triu_indices = np.triu_indices(neighbors_matrix.shape[0], 1)
        for i, j in zip(u_triu_indices[0], u_triu_indices[1]):
            pair = self.valid_pair(id_1=neighbors_matrix.index[i],
                                   id_2=neighbors_matrix.columns[j])
            neighbors_matrix.iloc[i, j] = pair
            if pair:
                penalty_matrix.iloc[i, j] = self.get_deadhead(id_1=penalty_matrix.index[i],
                                                              id_2=penalty_matrix.columns[j])

        return neighbors_matrix, penalty_matrix




