"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from ..utils import *

# Python
import numpy as np
from numpy import argmin

"""___Classes___________________________________________________________________________________"""


class Party(Deck):

    decks: List[Deck]

    energy: NDArray

    score: NDArray
    turn: int
    round: int
    winner: Optional[int]

    min_energy: NDArray
    max_energy: NDArray
    resource_per_turn: Dict[Literal["power", "energy"], List[NDArray]]

    def calculate_stats(self):
        self.stats = [
            self.get_stats(self.decks[0]),
            self.get_stats(self.decks[1]),
        ]

    def get_lock_statuses(self) -> List[Dict[str, int]]:
        lock_statuses = [{}, {}]
        for player in range(2):
            for carte in self.decks[player].main:
                lock_status = argmin(self.decks[player].cartes[carte].buff["lock"][2:])
                lock_statuses[player][carte] = lock_status
        return lock_statuses

    @property
    def players_rounds(self) -> List[int]:
        players_rounds = [0, 0]
        for round in range(self.rounds):
            round_score_player0 = np.sum(self.score[round, :, 0])
            round_score_player1 = np.sum(self.score[round, :, 1])
            if round_score_player0 > round_score_player1:
                players_rounds[0] += 1
            elif round_score_player1 > round_score_player0:
                players_rounds[1] += 1
        return players_rounds

    def count_turn(self) -> None:
        self.turn += 1
        if self.turn == self.turns:
            self.turn = 0
            self.round += 1
            self.check_end_game()

    def check_end_game(self) -> None:
        rounds_player0, rounds_player1 = self.players_rounds
        if self.rounds - self.round < rounds_player0 - rounds_player1:
            self.winner = 0
            self.end_game()
        elif self.rounds - self.round < rounds_player1 - rounds_player0:
            self.winner = 1
            self.end_game()
        elif self.round == self.rounds:
            self.winner = None
            self.end_game()

    def end_game(self) -> None:
        pass
