"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.game import Game

# Python
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestGame(Assert):

    def test_create_deck(self) -> None:
        game = Game()
        game.create_game(dummy_deck(), dummy_deck(), 100, 0, 100, 100)

    def test_play(self, game: Game) -> None:
        play0 = ["id0", "id1", None]
        play1 = ["id0", None, None]
        game.play(play0, play1)
        self.assertEqual(int(game.score[0, 0, 0]), 260 + 260)
        self.assertEqual(int(game.score[0, 0, 1]), 10)

    def test_count_turn(self, game: Game) -> None:
        play0 = [None, None, None]
        play1 = [None, None, None]
        for _ in range(game.turns):
            game.play(play0, play1)
        self.assertEqual(game.turn, 0)
        self.assertEqual(game.round, 1)
        self.assertEqual(game.winner, None)
        self.assertEqual(game.players_rounds, [0, 0])

    def test_winner0(self, game: Game) -> None:
        play0 = ["id0", None, None]
        play1 = [None, None, None]
        game.play(play0, play1)
        for _ in range(game.turns - 1 + (game.rounds - 1) * game.turns):
            game.play(play1, play1)
        self.assertEqual(0, game.winner)

    def test_winner1(self, game: Game) -> None:
        play0 = ["id0", None, None]
        play1 = [None, None, None]
        game.play(play1, play0)
        for _ in range(game.turns - 1 + (game.rounds - 1) * game.turns):
            game.play(play1, play1)
        self.assertEqual(1, game.winner)

    def test_winner2(self, game: Game) -> None:
        play1 = [None, None, None]
        game.play(play1, play1)
        for _ in range(game.turns - 1 + (game.rounds - 1) * game.turns):
            game.play(play1, play1)
        self.assertEqual(None, game.winner)
