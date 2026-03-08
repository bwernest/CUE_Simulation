"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .toolbox import ToolBox

# Python
from numpy.typing import NDArray
from typing import Dict, List

"""___Classes___________________________________________________________________________________"""


class GameUtility(ToolBox):

    def debuff_array(self, buff: NDArray) -> NDArray:
        unbuff = buff
        unbuff[2:-1] = buff[3:]
        unbuff[-1] = 0
        return unbuff
