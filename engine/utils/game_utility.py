"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .toolbox import ToolBox

# Python
from numpy.typing import NDArray
from random import sample
from typing import Dict, List

"""___Classes___________________________________________________________________________________"""


class GameUtility(ToolBox):

    def debuff_array(self, buff: NDArray) -> NDArray:
        unbuff = buff
        unbuff[2:-1] = buff[3:]
        unbuff[-1] = 0
        return unbuff

    def filter_targets_random(
        self,
        targets: Dict[int, List],
        filtre: List,
        player: int,
        card_id: str,
    ) -> Dict[int, List]:
        n_selected = int(filtre[1])
        len0, len1 = len(targets[0]), len(targets[1])
        if n_selected >= len0 + len1:
            return targets
        index_selected = sorted(sample([k for k in range(len0 + len1)], n_selected))
        selected = {}
        selected[0] = [targets[0][k] if k < len0 else None for k in index_selected]
        selected[1] = [targets[1][k - len0] if k >= len0 else None for k in index_selected]
        while None in selected[0]:
            selected[0].remove(None)
        while None in selected[1]:
            selected[1].remove(None)
        return selected
