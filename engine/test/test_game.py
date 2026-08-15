"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.game import Game

# Python
import pytest
from random import seed

"""___Tests_____________________________________________________________________________________"""


class TestGame(Assert):

    def test_create_deck(self) -> None:
        game = Game()
        _ = game.create_game(dummy_deck(), dummy_deck(), 100, 0, 100, 100)

    def test_play(self, game: Game, party: Party) -> None:
        play0 = ["id0", "id1", None]
        play1 = ["id0", None, None]
        party = game.play(party, play0, play1)
        self.assertEqual(int(party.score[0, 0, 0]), 260 + 260)
        self.assertEqual(int(party.score[0, 0, 1]), 10)

    def test_count_turn(self, game: Game, party: Party) -> None:
        play0 = [None, None, None]
        play1 = [None, None, None]
        for _ in range(game.turns):
            party = game.play(party, play0, play1)
        self.assertEqual(party.turn, 0)
        self.assertEqual(party.round, 1)
        self.assertEqual(party.winner, None)
        self.assertEqual(party.score_rounds, [0, 0])
        self.assertEqual(False, party.done)

    def test_winner0(self, game: Game, party: Party) -> None:
        play0 = ["id0", None, None]
        play1 = [None, None, None]
        party = game.play(party, play0, play1)
        for _ in range(game.turns - 1 + (game.rounds - 1) * game.turns):
            party = game.play(party, play1, play1)
        self.assertEqual(0, party.winner)
        self.assertEqual(True, party.done)

    def test_winner1(self, game: Game, party: Party) -> None:
        play0 = ["id0", None, None]
        play1 = [None, None, None]
        game.play(party, play1, play0)
        for _ in range(game.turns - 1 + (game.rounds - 1) * game.turns):
            game.play(party, play1, play1)
        self.assertEqual(1, party.winner)
        self.assertEqual(True, party.done)

    def test_winner2(self, game: Game, party: Party) -> None:
        play1 = [None, None, None]
        game.play(party, play1, play1)
        for _ in range(game.turns - 1 + (game.rounds - 1) * game.turns):
            game.play(party, play1, play1)
        self.assertEqual(None, party.winner)
        self.assertEqual(True, party.done)

    class TestGame_FilterRandom(Assert):

        def test_filtre_random1(self, game: Game, party: Party) -> None:
            targets = {arg: [] for arg in get_args(JoueurID)}
            expected = targets
            result = game.filter_targets_random(party, targets, ("random", "9", ""), 0, "")
            self.assertEqual(expected, result)

        def test_filtre_random2(self, game: Game, party: Party) -> None:
            targets = {get_args(JoueurID)[0]: ["a", "b", "c", "d", "e"], get_args(JoueurID)[1]: ["a", "b", "c", "d"]}
            expected = targets
            result = game.filter_targets_random(party, targets, ("random", "9", ""), 0, "")
            self.assertEqual(expected, result)

        def test_filtre_random3(self, game: Game, party: Party) -> None:
            seed(26)
            targets = {get_args(JoueurID)[0]: ["a", "b", "c", "d", "e"], get_args(JoueurID)[1]: ["a", "b", "c", "d"]}
            expected = {0: ["d"], 1: []}
            result = game.filter_targets_random(party, targets, ("random", "1", ""), 0, "")
            self.assertEqual(expected, result)

        def test_filtre_random4(self, game: Game, party: Party) -> None:
            seed(26)
            targets = {get_args(JoueurID)[0]: ["a", "b", "c", "d", "e"], get_args(JoueurID)[1]: ["a", "b", "c", "d"]}
            expected = {0: ["d", "e"], 1: ["a", "c", "d"]}
            result = game.filter_targets_random(party, targets, ("random", "5", ""), 0, "")
            self.assertEqual(expected, result)
