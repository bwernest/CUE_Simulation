"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from .game import Game
from .party import Party
from ..utils import *

# Python
from random import randint, shuffle
from typing import List

"""___Classes___________________________________________________________________________________"""


class Player(Party):

    def get_play(self, party: Party, player: Joueur, player_num: JoueurID) -> Play:
        return self.__getattribute__(player)(party, player_num)

    def Mallia(self, party: Party, player: JoueurID) -> Play:
        cards_ids = party.decks[player].main
        shuffle(cards_ids)
        index = 3
        play = cards_ids[:index] + [None] * (3 - index)
        while not party.check_play(play, player):
            shuffle(cards_ids)
            index -= 1
            play = cards_ids[:index] + [None] * (3 - index)
        return play
