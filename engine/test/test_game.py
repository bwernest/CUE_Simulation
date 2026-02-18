"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.game import Game

# Python
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestGame(Assert):

    def test_score(self) -> None:
        game = Game()
        game.create_game()
        expected = {
            1:{1:[None, None], 2:[None, None], 3:[None, None]},
            2:{1:[None, None], 2:[None, None], 3:[None, None]},
            3:{1:[None, None], 2:[None, None], 3:[None, None]},
            4:{1:[None, None], 2:[None, None], 3:[None, None]},
            5:{1:[None, None], 2:[None, None], 3:[None, None]},
        }
        result = game.score
        self.assertEqual(expected, result)
