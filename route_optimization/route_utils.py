from itertools import tee
import random

class InvalidVehicleError(Exception):
    pass


class InvalidScheduleError(Exception):
    pass


ID = 'Id'
ORIGIN = 'Origin'
DESTINATION = 'Destination'
DEPARTURE = 'Departure'
ARRIVAL = 'Arrival'
FORMAT = '%(asctime)s: %(message)s'
DEADHEAD = 15


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def random_element(s: set) -> int:
    return random.sample(s, 1)[0]


def partitions(A):
    if not A:
        yield []
    else:
        a, *R = A
        for partition in partitions(R):
            yield partition + [[a]]
            for i, subset in enumerate(partition):
                yield partition[:i] + [subset + [a]] + partition[i+1:]