from unittest import TestCase
from unittest import mock
import pandas as pd
from route_optimization.route_optimization_handler import ID, ORIGIN, DESTINATION, DEPARTURE, ARRIVAL, \
    RouteOptimizationHandler
from route_optimization.route_utils import InvalidVehicleError


class TestRouteOptimizationHandler(TestCase):
    def setUp(self) -> None:
        self.dummy_routes_df = pd.DataFrame([[2, 9, 305, 365],
                                             [1, 1, 720, 840],
                                             [1, 1, 840, 900]],
                                            columns=[ORIGIN, DESTINATION, DEPARTURE, ARRIVAL],
                                            index=[1, 27, 28])

        self.target = RouteOptimizationHandler(routes_df=self.dummy_routes_df, restricted_time=10)

    def test_get_deadheads(self):
        result = self.target.get_deadhead(id_1=1, id_2=27)
        self.assertEqual(first=15, second=result)
        result = self.target.get_deadhead(id_1=27, id_2=28)
        self.assertEqual(first=0, second=result)

    def test_get_deadheads_wrong_id(self):
        self.assertRaises(KeyError, RouteOptimizationHandler.get_deadhead, self.target, 100, 1)

    def test_valid_pair(self):
        result = self.target.valid_pair(id_1=1, id_2=27)
        self.assertTrue(expr=result)
        result = self.target.valid_pair(id_1=27, id_2=1)
        self.assertFalse(expr=result)

    def test_valid_pair_wrong_id(self):
        self.assertRaises(KeyError, RouteOptimizationHandler.valid_pair, self.target, 100, 1)

    def test_valid_vehicle(self):
        result = self.target.valid_vehicle(vehicle=[1, 27, 28])
        self.assertTrue(expr=result)
        result = self.target.valid_vehicle(vehicle=[1, 28, 27])
        self.assertFalse(expr=result)

    def test_deadhead_duration(self):
        result = self.target.deadhead_duration(vehicle=[1, 27, 28])
        self.assertEqual(first=45, second=result)

    def test_deadhead_duration_invalid_vehicle(self):
        self.assertRaises(InvalidVehicleError, RouteOptimizationHandler.deadhead_duration, self.target, [1, 28, 27])

    def test_t(self):
        result = self.target.valid_vehicle(vehicle=[])
        print(result)
        result = self.target.deadhead_duration(vehicle=[])
        print(result)