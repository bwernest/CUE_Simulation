"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from ..utils import *

# Python
import numpy as np
import numpy.typing as npt
from typing import Dict, List

"""___Classes___________________________________________________________________________________"""


class Game(Deck):

    decks: List[Deck]

    score: npt.NDArray
    turn: int
    round: int
    winner: int | None

    def create_game(self, deck0: Deck, deck1: Deck) -> None:
        self.decks = [deck0, deck1]
        self.score = np.zeros((self.rounds, self.turns, 2), dtype=int)
        self.turn = 0
        self.round = 0
        self.winner = None

    def play(self, play0: List[str | None], play1: List[str | None]) -> None:
        if not len(play0) == self.play_len or not len(play1) == self.play_len:
            raise PlayIncorrect("Nombre de cartes jouées incorrect")
        plays = [play0, play1]
        for player in range(2):
            for k in range(self.play_len):
                if plays[player][k] is None:
                    continue
                self.score[self.round, self.turn,
                           player] += self.decks[player].cards[plays[player][k]].power

        self.count_turn()

    def count_turn(self) -> None:
        self.turn += 1
        if self.turn == self.turns:
            self.turn = 0
            self.round += 1
            self.ckeck_end_game()

    def ckeck_end_game(self) -> None:
        rounds_player0 = np.sum(self.score[:self.round, :, 0])
        rounds_player1 = np.sum(self.score[:self.round, :, 1])
        if rounds_player0 > self.rounds // 2:
            self.winner = 0
        elif rounds_player1 > self.rounds // 2:
            self.winner = 1
