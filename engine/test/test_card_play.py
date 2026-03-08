"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

# Python
from numpy import array, sum, zeros

"""___Tests_____________________________________________________________________________________"""


class TestCardPlay(Assert):

    def test_card_MYPA001(self) -> None:
        game = unique_card_play("MYPA001")
        self.assertEqual(zeros((7), dtype=int), game.resource_per_turn["energy"][0])
        self.assertEqual(array([154, 0]), game.score[0, 0, :])
        self.assertEqual(array([100 - 7, 100]), game.energy)
        self.assertEqual({"album": {"paleontology": 1, "test_album": 17}, "collection": {
                         "paleontology mythic cards": 1, "test_collection": 17}}, game.stats[0])

    def test_card_PCA002(self) -> None:
        expected = array([72, 0])
        game = unique_card_play("PCA002")
        result = game.score[0, 0, :]
        self.assertEqual(expected, result)
        self.assertEqual(array([100 - 8, 100]), game.energy)

    def test_card_PAN015(self) -> None:
        game = unique_card_play("PAN015")
        self.assertEqual(array([83 + 24, 0]), game.score[0, 0, :])
        self.assertEqual(array([100 - 8, 100]), game.energy)

    def test_card_PCA038(self) -> None:
        game = unique_card_play("PCA038")
        self.assertEqual(array([65, 0]), game.score[0, 0, :])
        self.assertEqual(array([100 - 6 + 5, 100]), game.energy)

    def test_card_PHE017(self) -> None:
        game = unique_card_play("PHE017")
        self.assertEqual(array([76 + 8, 0]), game.score[0, 0, :])
        self.assertEqual(array([100 - 8, 100]), game.energy)
        self.assertEqual(array([8, 0, 0, 0, 0, 0, 0]),
                         game.decks[0].cards["phe017"].buff["power"])

    def test_card_PAN024(self) -> None:
        game = unique_card_play("PAN024")
        total_hand_buff = int(sum([sum(game.decks[0].cards[card_id].buff["power"])
                              for card_id in game.decks[0].hand]))
        self.assertEqual(46 * 2, total_hand_buff)
        self.assertIn(game.score[0, 0, 0], [40, 86])
        self.assertEqual(array([100 - 7, 100]), game.energy)

    def test_card_PHE026(self) -> None:
        game = unique_card_play("PHE026")
        self.assertEqual(array([3, 0, 0, 0, 0, 0, 0]), game.resource_per_turn["power"][0])
        self.assertEqual(array([68, 0]), game.score[0, 0, :])
        self.assertEqual(array([-1, 0, 0, 0, 0, 0, 0]), game.decks[0].cards["phe026"].buff["cost"])
        self.assertEqual(array([100 - 8 + 1, 100]), game.energy)
