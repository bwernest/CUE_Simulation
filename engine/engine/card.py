"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..utils import *

# Python
import numpy as np
from numpy.typing import NDArray
from pandas import isna
from typing import Dict, List, Literal

"""___Classes___________________________________________________________________________________"""


class Card(GameUtility):

    id: str
    name: str
    base_power: int
    base_cost: int
    attacks: Dict[str, List]

    def __eq__(self, value):
        if type(value) != self.__class__:
            return False
        for key in ["id", "name", "keywords", "base_power", "base_cost", "attacks", "album", "collection", "rarity", "type"]:
            if self.__dict__[key] != value.__dict__[key]:
                return False
        return True

    def __str__(self):
        return f"Card {self.name} / {self.album} / {self.collection}\nAttacks :\n{self.attacks}"

    @property
    def buff_dictionnary(self) -> Dict[Literal["power", "cost", "burn", "lock"], NDArray]:
        return {
            "power": np.zeros((self.buff_array_len), dtype=int),
            "cost": np.zeros((self.buff_array_len), dtype=int),
            "burn": np.zeros((self.buff_array_len), dtype=int),
            "lock": np.zeros((self.buff_array_len), dtype=int),
        }

    def create_card(
            self,
            id: str,
            name: str,
            keywords: List[str] = [],
            power: int = 0,
            cost: int = 0,
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
        self.base_cost = cost
        self.attack_name = attack_name
        self.album = album
        self.collection = collection
        self.rarity = rarity
        self.type = type
        self.attacks = self.attacks_dict
        self.reset_card()

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
        self.base_cost = int(infos[1][0])
        self.base_power = int(infos[1][1])
        column = 2
        self.keywords = []
        while not isna(infos[1][column]):
            self.keywords.append(str(infos[1][column]).lower())
            column += 1
        self.attacks = self.add_attacks(attacks)
        self.reset_card()

    def reset_card(self) -> None:
        self.played = 0
        self.buff = self.buff_dictionnary

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
            if info in ["condition", "acondition", "cible", "filtre"]:
                attacks_dict[atk][-1][info].append(self.clean_data_line(line[2:]))
            else:
                attacks_dict[atk][-1][info] = self.clean_data_line(line[2:])
        attacks_dict = self.convert_data(attacks_dict)
        return attacks_dict

    def convert_data(self, attacks_dict: Dict[str, List]) -> Dict[str, List]:
        for atk in attacks_dict.keys():
            pass
        return attacks_dict

    def clean_data_line(self, line: List) -> List:
        clean_line = []
        for item in line:
            if not isna(item):
                clean_line.append(str(item).lower())
        return clean_line
