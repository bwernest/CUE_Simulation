"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..parser.data_collector import DataCollector

"""___Tests_____________________________________________________________________________________"""


class TestDataCollector(Assert):

    def test_collect_data(self) -> None:
        data_collector = DataCollector("test")
        data_collector.collect_data()
        self.assertEqual(len(data_collector.cards) > 0, True)
