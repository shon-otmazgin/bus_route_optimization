from unittest import TestCase
import pandas as pd
from route_optimization.route_optimization_handler import ID, ORIGIN, DESTINATION, DEPARTURE, ARRIVAL, \
    RouteOptimizationHandler


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
        result = self.target.get_deadhead(id_1=1, id_2=100)
        self.assertIsNone(obj=result)
