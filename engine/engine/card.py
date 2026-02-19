"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..utils import *

# Python
from typing import List

"""___Classes___________________________________________________________________________________"""


class Card(ToolBox):

    id: str
    name: str
    power: int
    energy: int
    attacks: List

    def create_card(
            self,
            id: str,
            name: str,
            power: int = 100,
            energy: int = 10,
            attacks: List = None
            ) -> None:
        self.id = id
        self.name = name
        self.power = power
        self.energy = energy
        self.attacks = attacks if attacks is not None else []
