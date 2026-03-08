"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..utils.game_utility import GameUtility

# Python
from numpy import array
from random import seed

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

    def test_filtre_random1(self) -> None:
        gu = GameUtility("test")
        targets = {0: [], 1: []}
        expected = targets
        result = gu.filter_targets_random(targets, ["random", "9"])
        self.assertEqual(expected, result)

    def test_filtre_random2(self) -> None:
        gu = GameUtility("test")
        targets = {0: ["a", "b", "c", "d", "e"], 1: ["a", "b", "c", "d"]}
        expected = targets
        result = gu.filter_targets_random(targets, ["random", "9"])
        self.assertEqual(expected, result)

    def test_filtre_random3(self) -> None:
        gu = GameUtility("test")
        seed(26)
        targets = {0: ["a", "b", "c", "d", "e"], 1: ["a", "b", "c", "d"]}
        expected = {0: ["d"], 1: []}
        result = gu.filter_targets_random(targets, ["random", "1"])
        self.assertEqual(expected, result)

    def test_filtre_random4(self) -> None:
        gu = GameUtility("test")
        seed(26)
        targets = {0: ["a", "b", "c", "d", "e"], 1: ["a", "b", "c", "d"]}
        expected = {0: ["d", "e"], 1: ["a", "c", "d"]}
        result = gu.filter_targets_random(targets, ["random", "5"])
        self.assertEqual(expected, result)
