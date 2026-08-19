"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from .engine import Engine
from ..parser.data_collector import DataCollector
from ..utils import *

# Python
from copy import deepcopy
import numpy as np
from tqdm import tqdm
from typing import List

"""___Classes___________________________________________________________________________________"""


class Script(ToolBox):

    def championnat(self, players: List[Joueur], deck: Deck, n_game: int) -> None:

        # Initialisation
        engine = Engine("prod")
        lenP = len(players)
        score_board: List[List[str]] = [["//" for _ in range(lenP + 1)] for _ in range(lenP + 1)]
        leaderboard = [[player, 0] for player in players]
        deckbis = deepcopy(deck)
        n_match = 0
        score_board[0][1:] = players
        for p, player in enumerate(players):
            score_board[p + 1][0] = player
        self.add_log("Début du championnat")
        self.add_log(f"Il y aura {(int(lenP**2 - lenP) / 2)} journées.")

        # Boucle
        for j1, J1 in enumerate(players):
            for j2, J2 in enumerate(players):
                if j1 == j2 or score_board[j1 + 1][j2 + 1] != "//":
                    continue

                # Match
                score = [0, 0, 0]
                n_match += 1
                self.add_log(f"J{n_match} : {J1} VS {J2}")
                for _ in tqdm(range(n_game)):
                    party = engine.fight(deck, deckbis, J1, J2)
                    score[{0: 0, 1: 1, None: 2}[party.winner]] += 1
                score_board[j1 + 1][j2 + 1] = str(int(score[0] / n_game * 100))
                score_board[j2 + 1][j1 + 1] = str(int(score[1] / n_game * 100))
                leaderboard[j1][1] += self.get_match_points(score, 0)
                leaderboard[j2][1] += self.get_match_points(score, 1)

        # Score Board
        score_board[0][0] = "CUE"
        self.export_score_board(score_board)

        # Leaderboard
        for i in range(len(leaderboard)):
            for j in range(len(leaderboard) - i - 1):
                if leaderboard[j][1] < leaderboard[j + 1][1]:
                    temp = leaderboard[j]
                    leaderboard[j] = leaderboard[j + 1]
                    leaderboard[j + 1] = temp
        self.add_log("Classement final :")
        for l, line in enumerate(leaderboard):
            self.add_log(f"{l + 1} - {line[0]}\t{line[1]}")

    def get_match_points(self, score: List[int], player: JoueurID) -> int:
        n_game = sum(score)
        if score[0] == score[1]:
            return 1
        return 3 if round(score[player] / (n_game - score[2]), 2) > 0.50 else 0

    def export_score_board(self, score_board: List[List[str]]) -> None:
        txt = "\n".join(["\t".join(line) for line in score_board])
        self.write_txt(self.paths["file_save"], txt)
