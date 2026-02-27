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

    def start_engine(self) -> None:
        self.collect_data()

    def start_game(self, deck1: Deck, deck2: Deck, shuffle: bool = True) -> None:
        self.game = Game()
        self.game.create_game(deck1, deck2)
        self.game.start_game(shuffle=shuffle)

    def play(self, play0: List[str | None], play1: List[str | None]) -> None:
        self.game.play(play0, play1)
