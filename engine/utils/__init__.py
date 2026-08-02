"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .errors import *
from .game_utility import GameUtility
from .toolbox import ToolBox

# Python
import os
from numpy.typing import NDArray
from typing import Callable, Dict, List, Literal, Optional, Tuple
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
