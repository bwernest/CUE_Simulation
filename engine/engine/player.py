"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from .game import Game
from .party import Party
from ..utils import *

# Python
from random import randint, shuffle
from tqdm import tqdm
from typing import List

"""___Classes___________________________________________________________________________________"""


class Player(Game):

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

    def Mauvaka(self, party: Party, player: JoueurID) -> Play:
        cards_ids = party.decks[player].main
        plays = party.get_all_plays(cards_ids, player)
        best_play = plays[0]
        play0, play1 = {
            0: (best_play, [None] * 3),
            1: ([None] * 3, best_play),
        }[player]
        forward_party = self.play(party, play0, play1)
        best_score = forward_party.last_score[player]
        for play in plays[1:]:
            play0, play1 = {
                0: (best_play, [None] * 3),
                1: ([None] * 3, best_play),
            }[player]
            forward_party = self.play(party, play0, play1)
            score = forward_party.last_score[player]
            if score > best_score:
                best_score = score
                best_play = play
        return best_play
