"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..utils import *

# Python
from pandas import isna
from typing import List

"""___Classes___________________________________________________________________________________"""


class Card(ToolBox):

    id: str
    name: str
    power: int
    energy: int
    attacks: List

    def __eq__(self, value):
        if not isinstance(value, Card):
            return False
        return self.id == value.id and self.name == value.name and self.power == value.power and self.energy == value.energy

    def create_card(
            self,
            id: str,
            name: str,
            power: int = 0,
            energy: int = 0,
            attack_name: str | None = None,
            album: str | None = None,
            collection: str | None = None,
            rarity: str | None = None,
            type: str | None = None
    ) -> None:
        self.id = id.lower()
        self.name = name.lower()
        self.power = power
        self.energy = energy
        self.attack_name = attack_name
        self.album = album
        self.collection = collection
        self.rarity = rarity
        self.type = type

    def create_card_from_data(
            self,
            data: List
    ) -> None:
        infos, attacks = self.split_data(data)
        self.id = infos[0][0].lower()
        self.name = infos[0][1].lower()
        if isna(infos[0][2]):
            self.attack_name = None
        else:
            self.attack_name = infos[0][2].lower()
        self.album = infos[0][3].lower()
        self.collection = infos[0][4].lower()
        self.rarity = infos[0][5].lower()
        self.type = infos[0][6].lower()
        self.energy = int(infos[1][0])
        self.power = int(infos[1][1])
        self.attacks = attacks

    def split_data(self, data: List) -> tuple:
        infos = data[:2]
        attacks = data[2:]
        return infos, attacks
