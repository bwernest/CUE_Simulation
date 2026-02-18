"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .card import Card
from ..utils import *

# Python
from typing import List

"""___Classes___________________________________________________________________________________"""


class Deck(Card):

    cards: List[Card]

    def create(self) -> None:
        pass
