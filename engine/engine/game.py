"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from ..utils import *

# Python
from typing import Dict

"""___Classes___________________________________________________________________________________"""


class Game(Deck):

    deck1: Deck
    deck2: Deck

    score: Dict

    def create_game(self) -> None:
        
        self.score = {k:{l:[None, None] for l in range(1, 4)} for k in range(1, 6)}
