"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.card import Card

# Python
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestCard(Assert):

    def test_create_card(self) -> None:
        card = Card("test")