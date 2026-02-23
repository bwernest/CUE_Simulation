"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..parser.data_collector import DataCollector

from .game import Game
from ..utils import *

"""___Classes___________________________________________________________________________________"""


class Engine(DataCollector):

    def start(self) -> None:
        self.collect_data()

    def start_game(self) -> None:
        self.game = Game()
        self.game.create_game()
