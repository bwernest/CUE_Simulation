"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from .party import Party
from .player import Player
from ..parser.data_collector import DataCollector
from ..utils import *

# Python
from typing import List

"""___Classes___________________________________________________________________________________"""


class Engine(DataCollector, Player):

    def start_engine(self, recyclage: bool = False) -> None:
        self.add_log("Collecte des données.")
        self.collect_data(recyclage)

    def __eq__(self, value: Any) -> bool:
        return False

    def fight(
            self,
            player_deck: Deck,
            opponent_deck: Deck,
            player: Joueur,
            opponent: Joueur,
    ) -> Party:
        party = self.create_game(player_deck, opponent_deck, 20, 21, 12, 250)
        party = self.start_game(party)
        while not party.done:
            player_play = self.get_play(party, player, 0)
            opponent_play = self.get_play(party, opponent, 1)
            party = self.play(party, player_play, opponent_play)
        return party
