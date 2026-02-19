"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.game import Game

# Python
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestGame(Assert):

    def test_create_deck(self, dummy_deck: Deck) -> None:
        game = Game()
        game.create_game(dummy_deck, dummy_deck)

    def test_play(self, game: Game) -> None:
        play0 = ["id0", "id1", None]
        play1 = ["id0", None, None]
        game.play(play0, play1)
        self.assertEqual(int(game.score[0, 0, 0]), 260+260)
        self.assertEqual(int(game.score[0, 0, 1]), 10)
