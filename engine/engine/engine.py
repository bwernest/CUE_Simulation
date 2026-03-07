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
        self.add_log("Collecte des données.")
        self.collect_data()

    def start_game(self, deck1: Deck, deck2: Deck, start_energy: int, energy_per_turn: int, min_energy: int, max_energy: int, shuffle: bool = True) -> None:
        self.game = Game()
        self.game.create_game(deck1, deck2, start_energy, energy_per_turn, min_energy, max_energy)
        self.game.start_game(shuffle=shuffle)

    def play(self, play0: List[str | None], play1: List[str | None]) -> None:
        self.game.play(play0, play1)
