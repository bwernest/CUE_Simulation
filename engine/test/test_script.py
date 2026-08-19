"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.script import Script

# Python
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestScript(Assert):

    def test_get_match_points_1(self, script: Script) -> None:
        expected = 3
        result = script.get_match_points([1, 0, 0], 0)
        self.assertEqual(expected, result)

    def test_get_match_points_2(self, script: Script) -> None:
        expected = 0
        result = script.get_match_points([0, 1, 0], 0)
        self.assertEqual(expected, result)

    def test_get_match_points_3(self, script: Script) -> None:
        expected = 1
        result = script.get_match_points([0, 0, 1], 0)
        self.assertEqual(expected, result)

    def test_get_match_points_4(self, script: Script) -> None:
        expected = 0
        result = script.get_match_points([1, 0, 0], 1)
        self.assertEqual(expected, result)

    def test_get_match_points_5(self, script: Script) -> None:
        expected = 3
        result = script.get_match_points([0, 1, 0], 1)
        self.assertEqual(expected, result)

    def test_get_match_points_6(self, script: Script) -> None:
        expected = 1
        result = script.get_match_points([0, 0, 1], 1)
        self.assertEqual(expected, result)

    def test_get_match_points_7(self, script: Script) -> None:
        expected = 1
        result = script.get_match_points([5, 5, 0], 0)
        self.assertEqual(expected, result)

    def test_get_match_points_8(self, script: Script) -> None:
        expected = 1
        result = script.get_match_points([5, 5, 0], 1)
        self.assertEqual(expected, result)
