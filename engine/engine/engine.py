"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from .game import Game
from ..parser.data_collector import DataCollector
from ..utils import *

# Python
from typing import List

"""___Classes___________________________________________________________________________________"""


class Engine(DataCollector):

    def start_engine(self, recyclage: bool = False) -> None:
        self.add_log("Collecte des données.")
        self.collect_data(recyclage)
