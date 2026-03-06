"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.card import Card
from ..engine.engine import Engine

# Python
import numpy as np
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestCardPlay(Assert):

    def test_card_MYPA001(self) -> None:
        expected = np.array([154, 0])
        game = unique_card_play("MYPA001")
        result = game.score[0, 0, :]
        self.assertEqual(expected, result)
