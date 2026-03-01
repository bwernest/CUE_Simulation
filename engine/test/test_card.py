"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.card import Card
from ..engine.engine import Engine

# Python
import numpy as np
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestCard(Assert):

    def test_create_card(self) -> None:
        _ = Card("test")

    def test_card_MYPA001(self) -> None:
        expected = np.array([77, 0])
        game = unique_card_play("MYPA001")
        result = game.score[0, 0, :]
        self.assertEqual(expected, result)

    def test_card_equal(self, engine: Engine) -> None:
        expected = True
        card1 = engine.cards["mypa001"]
        card2 = engine.cards["mypa001"]
        result = card1 == card2
        self.assertEqual(expected, result)

    def test_card_not_equal1(self, engine: Engine) -> None:
        expected = False
        card1 = engine.cards["mypa001"]
        card2 = engine.cards["pan015"]
        result = card1 == card2
        self.assertEqual(expected, result)

    def test_card_not_equal2(self, engine: Engine) -> None:
        expected = False
        card1 = engine.cards["pan015"]
        result = card1 == engine
        self.assertEqual(expected, result)
