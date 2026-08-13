"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from .toolbox import ToolBox

# Python
from numpy.typing import NDArray
from typing import TypeVar
U = TypeVar("U")
V = TypeVar("V")

"""___Classes___________________________________________________________________________________"""


class GameUtility(ToolBox):

    def debuff_array(self, buff: NDArray) -> NDArray:
        unbuff = buff
        unbuff[2:-1] = buff[3:]
        unbuff[-1] = 0
        return unbuff

    def merge_dict(self, dict1: Dict[U, V], dict2: Dict[U, V]) -> Dict[U, V]:
        merged = {}
        for key in dict1.keys():
            merged[key] = dict1[key] + dict2[key]   # type:ignore
        return merged
