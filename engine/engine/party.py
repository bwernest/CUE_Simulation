"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from ..utils import *

# Python
import numpy as np
from numpy import argmin

"""___Classes___________________________________________________________________________________"""


class Party(Deck):
    """
    Party
    -----
    Classe permettant de sauvegarder une partie. Une instance est créée lors de la création d'une
    partie. Le jeu CUE interragi avec cette instance pour faire avancer la partie.

    Cette classe permet de consulter les informations sur la partie en cours ou terminées. De plus
    c'est grâce à des sauvegardes intermédiaires qu'elle permet de simuler des Play.
    """

    decks: List[Deck]

    energy: NDArray

    arenas = [
        "paleontology",
        "Space",
        "History",
        "Life on Land",
        "Oceans and Seas",
    ]

    score: NDArray
    turn: int
    round: int
    winner: Optional[int]

    min_energy: NDArray
    max_energy: NDArray
    resource_per_turn: Dict[Literal["power", "energy"], List[NDArray]]

    @property
    def arena(self) -> str:
        return self.arenas[self.round]

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
    def score_rounds(self) -> List[int]:
        score_rounds = [0, 0]
        for round in range(self.round):
            round_score_player0 = np.sum(self.score[round, :, 0])
            round_score_player1 = np.sum(self.score[round, :, 1])
            if round_score_player0 > round_score_player1:
                score_rounds[0] += 1
            elif round_score_player1 > round_score_player0:
                score_rounds[1] += 1
        return score_rounds

    def count_turn(self) -> None:
        self.turn += 1
        if self.turn == self.turns:
            self.turn = 0
            self.round += 1
            self.check_end_game()

    def check_end_game(self) -> None:
        rounds_player0, rounds_player1 = self.score_rounds
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
