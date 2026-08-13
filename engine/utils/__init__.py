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

Album = Literal[
    "Arts & Culture",
    "History",
    "Life on Land",
    "Oceans and Seas",
    "Paleontology",
    "Science",
    "Space",
]

Collection = Literal[
    "Ancient Creatures",
    "Carnivores",
    "Fearsome Flyers",
    "Groundbreakers",
    "Herbivores",
    "Hoaxes and Cons",
    "Ice Age",
    "Land Before Time",
    "Monsters of The Deep",
    "Omnivores",
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

AttackFiltre = List[Literal["base_power", "base_cost", "rarity", "type", "random", "other"]]

Trigger = Literal["draw", "start", "play", "return"]
AttackInfo = Literal["condition", "acondition", "cible", "filtre", "afiltre", "effet", "multiplicateur", "duree"]
Attack = Dict[AttackInfo, List]
Attacks = Dict[Trigger, List[Attack]]
