"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .errors import *
from .game_utility import GameUtility
from .toolbox import ToolBox

# Python
import os
from numpy.typing import NDArray
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple
from typing import get_args
import sys

"""___Literal___________________________________________________________________________________"""

Keyword = Literal[
    "beetle",
    "emperor",
    "mega",
]

Album = Literal[
    "arts & culture",
    "history",
    "life on land",
    "oceans and seas",
    "paleontology",
    "science",
    "space",
]

Collection = Literal[
    "ancient creatures",
    "carnivores",
    "fearsome flyers",
    "groundbreakers",
    "herbivores",
    "hoaxes and cons",
    "human evolution",
    "ice age",
    "land before time",
    "monsters of the deep",
    "omnivores",
]

Effect = Literal[
    "burn",
    "cost",
    "lock",
    "power",
]

CarteID = str
JoueurID = Literal[0, 1]
TargetsCarte = Dict[JoueurID, List[CarteID]]
TargetsJoueur = Dict[JoueurID, List[JoueurID]]
Targets = TargetsCarte | TargetsJoueur

Play = List[CarteID] | List[None] | List[Optional[CarteID]]

BuffArray = NDArray

Ressource = Literal["power", "energy"]
RessourcePerTurn = Dict[Ressource, List[BuffArray]]

StrNumber = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
AttackFiltre = Tuple[
    Literal["base_power", "base_cost", "played", "rarity", "type", "random", "other"],
    Literal["<", ">", "=", StrNumber],
    str,
]

Trigger = Literal["draw", "start", "play", "return"]
AttackInfo = Literal["condition", "acondition", "cible", "filtre", "afiltre", "effet", "multiplicateur", "duree"]
Attack = Dict[AttackInfo, List]
Attacks = Dict[Trigger, List[Attack]]
