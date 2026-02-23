"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..engine.card import Card
from ..engine.game import Game
from ..utils import *

# Python
from typing import Dict, Iterable, List

"""___Classes___________________________________________________________________________________"""


class DataCollector(Game):

    cards: Dict[str, Card]

    def collect_data(self) -> Dict[str, Card]:

        return self.cards
