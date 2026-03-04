"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..utils import *

# Python
from pandas import isna
from typing import Dict, List

"""___Classes___________________________________________________________________________________"""


class Card(ToolBox):

    id: str
    name: str
    base_power: int
    base_energy: int
    attacks: Dict[str, List]

    def __eq__(self, value):
        if type(value) != self.__class__:
            return False
        for key in ["id", "name", "keywords", "power", "energy", "attacks", "album", "collection", "rarity", "type"]:
            if self.__dict__[key] != value.__dict__[key]:
                return False
        return True

    def __str__(self):
        return f"Card {self.name}\nAttacks :\n{self.attacks}"

    def create_card(
            self,
            id: str,
            name: str,
            keywords: List[str] = [],
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
        self.keywords = keywords
        self.base_power = power
        self.base_energy = energy
        self.buff = {"power": [], "energy": [], "burn": []}
        self.attack_name = attack_name
        self.album = album
        self.collection = collection
        self.rarity = rarity
        self.type = type
        self.attacks = self.attacks_dict

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
        self.base_energy = int(infos[1][0])
        self.base_power = int(infos[1][1])
        self.buff = {"power": [], "energy": [], "burn": []}
        column = 2
        self.keywords = []
        while not isna(infos[1][column]):
            self.keywords.append(str(infos[1][column]).lower())
            column += 1
        self.attacks = self.add_attacks(attacks)

    def split_data(self, data: List) -> tuple:
        infos = data[:2]
        attacks = data[2:]
        return infos, attacks

    @property
    def attacks_dict(self) -> Dict[str, List]:
        return {
            "draw": [],
            "start": [],
            "play": [],
            "return": [],
        }

    def add_attacks(self, attacks: List) -> Dict[str, List]:
        attacks_dict = self.attacks_dict
        for line in attacks:
            info = line[1].lower()
            if not isna(line[0]):
                atk = line[0].lower()
                attacks_dict[atk].append({
                    "condition": [],
                    "acondition": [],
                    "cible": [],
                    "filtre": [],
                    "effet": [],
                    "multiplicateur": [],
                    "duree": [],
                })
            attacks_dict[atk][-1][info] = self.clean_data_line(line[2:])
        return attacks_dict

    def clean_data_line(self, line: List) -> List:
        clean_line = []
        for item in line:
            if not isna(item):
                clean_line.append(str(item).lower())
        return clean_line
