"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from ..utils import *

# Python
from itertools import combinations, permutations
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

    decks: Tuple[Deck, Deck]
    done: bool

    energie: NDArray

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
    resource_per_turn: RessourcePerTurn

    def __str__(self):
        return "Party"

    def __eq__(self, value: Party):
        for attribut in [
            "turn",
            "round",
            "score",
            "winner",
            "done",
            "min_energy",
            "max_energy",
            "resource_per_turn",
        ]:
            self.compare_attributs(attribut, self, value)
        if not self.decks[0] == value.decks[0]:
            print("Deck player différents !")
            return False
        if not self.decks[1] == value.decks[1]:
            print("Deck opponent différents !")
            return False
        return True

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
        """
        count_turn
        ----------
        Incrémente les compteurs de tours et de rounds.
        Vérfifie si la partie est terminée.
        """
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
        self.done = True
        return

    def get_amount(self, player: JoueurID, set_type: Literal["album", "collection"], set_name: Album | Collection) -> int:
        try:
            return self.stats[player][set_type][set_name]
        except KeyError:
            return 0

    def get_keyword_amount(self, player: JoueurID, keyword: Keyword) -> int:
        compte = 0
        for carte in self.decks[player].cartes.values():
            if keyword in carte.keywords:
                compte += 1
        return compte

    def check_play(self, play: Play, player: JoueurID) -> bool:
        cost = 0
        for cid in play:
            if cid is not None:
                # En main
                if cid not in self.decks[player].main:
                    return False

                carte = self.decks[player].cartes[cid]
                # Lock
                if carte.is_locked():
                    return False
                # Coût
                cost += carte.cost
        if cost > self.energie[player]:
            return False
        return True

    def show_score(self) -> None:
        # print(f"Round score {self.score_rounds}")
        print(f"W{'N' if self.winner is None else self.winner} en R{self.round} : " + " / ".join([f"R{k + 1} {np.sum(self.score[k, :], axis=0)}" for k in range(self.round)]))
        # print(" / ".join([f"R{k + 1} {self.score[k, 0]} {self.score[k, 1]} {self.score[k, 2]}" for k in range(self.round)]))

    def get_all_plays(self, cards_ids: List[CarteID], player: JoueurID) -> List[Play]:
        plays = [p for p in combinations(cards_ids, 3) if self.check_play(p, player)]
        if len(plays) == 0:
            plays += [list(p) + [None] for p in combinations(cards_ids, 2) if self.check_play(list(p) + [None], player)]
        if len(plays) == 0:
            plays += [list(p) + [None, None] for p in combinations(cards_ids, 1) if self.check_play(list(p) + [None, None], player)]
        return plays    # type:ignore

    @property
    def last_score(self) -> NDArray:
        if self.turn == 0:
            if self.round == 0:
                return self.score[0, 0]
            else:
                return self.score[self.round - 1][self.turns - 1]
        return self.score[self.round][self.turn - 1]

    def get_deck_power(self, player: JoueurID) -> int:
        return sum([carte.base_power + sum(carte.buff["power"]) for carte in self.decks[player].cartes.values()])
