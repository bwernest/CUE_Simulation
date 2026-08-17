"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..utils import *

# Python
import numpy as np
from pandas import isna

"""___Classes___________________________________________________________________________________"""


class Carte(GameUtility):

    id: str
    name: str
    base_power: int
    base_cost: int
    attacks: Dict[Trigger, List[Attack]]
    keywords: List[Keyword]
    album: Album
    collection: Collection

    def __eq__(self, value: Carte):
        if type(value) != Carte:
            return False
        for key in ["id", "name", "keywords", "base_power", "base_cost", "attacks", "album", "collection", "rarity", "type"]:
            if self.__dict__[key] != value.__dict__[key]:
                return False
        return True

    def __str__(self):
        return f"Carte {self.id}"

    @property
    def _buff_dictionnary(self) -> Dict[Effect, NDArray]:
        return {
            "power": np.zeros((self.buff_array_len), dtype=int),
            "cost": np.zeros((self.buff_array_len), dtype=int),
            "burn": np.zeros((self.buff_array_len), dtype=int),
            "lock": np.zeros((self.buff_array_len), dtype=int),
        }

    def is_locked(self) -> bool:
        return sum(self.buff["lock"]) > 0

    def create_carte(
            self,
            id: str,
            name: str,
            keywords: List[Keyword] = [],
            power: int = 0,
            cost: int = 0,
            attack_name: Optional[str] = None,
            album: Optional[str] = None,
            collection: Optional[str] = None,
            rarity: Optional[str] = None,
            type: Optional[str] = None
    ) -> None:
        self.id = id.lower()
        self.name = name.lower()
        self.keywords = keywords
        self.base_power = power
        self.base_cost = cost
        self.attack_name = attack_name
        self.album = album  # type:ignore
        self.collection = collection    # type:ignore
        self.rarity = rarity
        self.type = type
        self.attacks = self.attacks_dict
        self.reset_carte()

    def create_carte_from_data(
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
            self.keywords.append(str(infos[1][column]).lower())  # type:ignore
            column += 1
        self.attacks = self.add_attacks(attacks)
        self.reset_carte()

    def reset_carte(self) -> None:
        self.played = 0
        self.buff = self._buff_dictionnary

    def split_data(self, data: List) -> tuple:
        infos = data[:2]
        attacks = data[2:]
        return infos, attacks

    @property
    def attacks_dict(self) -> Dict[Trigger, List]:
        return {
            "draw": [],
            "start": [],
            "play": [],
            "return": [],
        }

    def add_attacks(self, attacks: List) -> Attacks:
        attacks_dict = self.attacks_dict
        for line in attacks:
            info: AttackInfo = line[1].lower()
            if not isna(line[0]):
                atk: Trigger = line[0].lower()
                attacks_dict[atk].append({
                    "condition": [],
                    "acondition": [],
                    "cible": [],
                    "filtre": [],
                    "afiltre": [],
                    "effet": [],
                    "multiplicateur": [],
                    "duree": [],
                })
            if info in ["condition", "acondition", "cible", "filtre", "afiltre"]:
                attacks_dict[atk][-1][info].append(self.clean_data_line(line[2:]))
            else:
                attacks_dict[atk][-1][info] = self.clean_data_line(line[2:])
        return attacks_dict

    def clean_data_line(self, line: List) -> List:
        clean_line = []
        for item in line:
            if not isna(item):
                clean_line.append(str(item).lower())
        return clean_line
