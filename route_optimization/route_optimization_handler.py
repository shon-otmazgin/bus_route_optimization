import pandas as pd
import numpy as np
import random
from itertools import tee
import math

ID = 'Id'
ORIGIN = 'Origin'
DESTINATION = 'Destination'
DEPARTURE = 'Departure'
ARRIVAL = 'Arrival'


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class RouteOptimizationHandler:
    def __init__(self, routes_df: pd.DataFrame, restricted_time: int):
        self.routes_df = routes_df
        self.restricted_time = restricted_time
        self.N = set(self.routes_df.index)

    def get_deadhead(self, id_1: int, id_2: int) -> int:
        try:
            return 15 if self.routes_df.loc[id_1][DESTINATION] != self.routes_df.loc[id_2][ORIGIN] else 0
        except KeyError as e:
            print(f'KeyError, no index {e} in routes df')
            return None




