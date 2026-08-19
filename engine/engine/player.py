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
        return self.get_best_play_power_turn(party, player)[0]

    def Noves(self, party: Party, player: JoueurID) -> Play:
        return self.get_best_play_power_deck(party, player)[0]

    def Mola(self, party: Party, player: JoueurID) -> Play:
        # Dernier tour
        if party.round == party.rounds - 1 and party.turn == party.turns - 1:
            return self.Noves(party, player)

        # Pas dernier tour
        cards_ids = party.decks[player].main
        plays = party.get_all_plays(cards_ids, player)
        best_score = 0
        best_play = [None, None, None]
        for play in plays:
            play0, play1 = {
                0: (play, [None] * 3),
                1: ([None] * 3, play),
            }[player]
            forward_party_1 = self.play(party, play0, play1)
            _, score = self.get_best_play_power_deck(forward_party_1, player)
            if score > best_score:
                best_score = score
                best_play = play
        return best_play    # type:ignore

    def Jelonch(self, party: Party, player: JoueurID) -> Play:
        if party.score_rounds[1 - player] == 2:
            return self.Mauvaka(party, player)
        else:
            return self.Noves(party, player)

    def Willis(self, party: Party, player: JoueurID) -> Play:
        """
        Willis : Mola puis Mauvaka à X-2
        """
        if party.score_rounds[1 - player] == 2:
            return self.Mauvaka(party, player)
        else:
            return self.Mola(party, player)

    def Graou(self, party: Party, player: JoueurID) -> Play:
        if party.score_rounds[player] == 2:
            return self.Mauvaka(party, player)
        else:
            return self.Noves(party, player)

    def Barassi(self, party: Party, player: JoueurID) -> Play:
        """
        Barassi : Mola puis Mauvaka à 2-X
        """
        if party.score_rounds[0] == 2:
            return self.Mauvaka(party, player)
        else:
            return self.Mola(party, player)

    def get_best_play_power_deck(self, party: Party, player: JoueurID) -> Tuple[Play, int]:
        cards_ids = party.decks[player].main
        plays = party.get_all_plays(cards_ids, player)
        best_play = [None, None, None]
        best_score = 0
        for play in plays:
            play0, play1 = {
                0: (play, [None] * 3),
                1: ([None] * 3, play),
            }[player]
            forward_party = self.play(party, play0, play1)
            score = forward_party.get_deck_power(player)
            if score > best_score:
                best_score = score
                best_play = play
        return best_play, best_score    # type:ignore

    def get_best_play_power_turn(self, party: Party, player: JoueurID) -> Tuple[Play, int]:
        cards_ids = party.decks[player].main
        plays = party.get_all_plays(cards_ids, player)
        best_play = [None, None, None]
        best_score = 0
        for play in plays[1:]:
            play0, play1 = {
                0: (play, [None] * 3),
                1: ([None] * 3, play),
            }[player]
            forward_party = self.play(party, play0, play1)
            score = forward_party.last_score[player]
            if score > best_score:
                best_score = score
                best_play = play
        return best_play, best_score    # type:ignore
