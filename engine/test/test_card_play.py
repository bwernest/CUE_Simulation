"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

# Python
import numpy as np

"""___Tests_____________________________________________________________________________________"""


class TestCardPlay(Assert):

    def test_card_MYPA001(self) -> None:
        game = unique_card_play("MYPA001")
        self.assertEqual(np.array([154, 0]), game.score[0, 0, :])
        self.assertEqual(np.array([100 - 7, 100]), game.energy)
        self.assertEqual({"album": {"paleontology": 1, "test_album": 17}, "collection": {
                         "paleontology mythic cards": 1, "test_collection": 17}}, game.stats[0])

    def test_card_PCA002(self) -> None:
        expected = np.array([72, 0])
        game = unique_card_play("PCA002")
        result = game.score[0, 0, :]
        self.assertEqual(expected, result)
        self.assertEqual(np.array([100 - 8, 100]), game.energy)

    def test_card_PCA038(self) -> None:
        expected = np.array([65, 0])
        game = unique_card_play("PCA038")
        result = game.score[0, 0, :]
        self.assertEqual(expected, result)
