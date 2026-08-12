"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..utils.game_utility import GameUtility

# Python
from numpy import array

"""___Tests_____________________________________________________________________________________"""


class TestGameUtility(Assert):

    def test_debuff_array1(self) -> None:
        gu = GameUtility("test")
        expected = array([1, 2, 4, 5, 6, 7, 8, 0])
        result = gu.debuff_array(array([1, 2, 3, 4, 5, 6, 7, 8]))
        self.assertEqual(expected, result)

    def test_debuff_array2(self) -> None:
        gu = GameUtility("test")
        expected = array([0, 0, 20, 20, 20, 20, 20, 0])
        result = gu.debuff_array(array([0, 0, 42, 20, 20, 20, 20, 20]))
        self.assertEqual(expected, result)
