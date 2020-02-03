from itertools import tee


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