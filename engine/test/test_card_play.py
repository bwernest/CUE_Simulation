"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

# Python
from numpy import array, sum, zeros

"""___Tests_____________________________________________________________________________________"""


class TestCardPlay(Assert):

    def test_card_MYPA001(self) -> None:
        game = unique_card_play("MYPA001")
        card = game.decks[0].cards["mypa001"]
        self.assertEqual(zeros((7), dtype=int), game.resource_per_turn["energy"][0])
        self.assertEqual(card.base_power + 77, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        self.assertEqual({"album": {"paleontology": 1, "test_album": 17}, "collection": {
                         "paleontology mythic cards": 1, "test_collection": 17}}, game.stats[0])

    def test_card_PCA002(self) -> None:
        game = unique_card_play("PCA002")
        card = game.decks[0].cards["pca002"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])

    def test_card_PAN015(self) -> None:
        game = unique_card_play("PAN015")
        card = game.decks[0].cards["pan015"]
        self.assertEqual(card.base_power + 24, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        self.assertEqual(array([0, 0, 0, 0, 0, 0, 0]), card.buff["power"])
        self.assertEqual(array([0, 0, -1, 0, 0, 0, 0]), card.buff["cost"])

    def test_card_PCA038(self) -> None:
        game = unique_card_play("PCA038")
        card = game.decks[0].cards["pca038"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(array([100 - card.base_cost + 5, 100]), game.energy)

    def test_card_PHE017(self) -> None:
        game = unique_card_play("PHE017")
        card = game.decks[0].cards["phe017"]
        self.assertEqual(card.base_power + 8, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        self.assertEqual(array([8, 0, 0, 0, 0, 0, 0]), card.buff["power"])

    def test_card_PAN024(self) -> None:
        game = unique_card_play("PAN024")
        card = game.decks[0].cards["pan024"]
        total_hand_buff = int(sum([sum(game.decks[0].cards[card_id].buff["power"])
                              for card_id in game.decks[0].hand]))
        self.assertIn(total_hand_buff, [46, 46 * 2])
        self.assertIn(game.score[0, 0, 0], [card.base_power, card.base_power + 46])
        self.assertEqual(100 - card.base_cost, game.energy[0])

    def test_card_PHE026(self) -> None:
        game = unique_card_play("PHE026")
        card = game.decks[0].cards["phe026"]
        self.assertEqual(array([3, 0, 0, 0, 0, 0, 0]), game.resource_per_turn["power"][0])
        self.assertEqual(card.base_power + 3, game.score[0, 0, 0])
        self.assertEqual(array([-1, 0, 0, 0, 0, 0, 0]), card.buff["cost"])
        self.assertEqual(100 - card.base_cost + 1, game.energy[0])

    def test_card_PAN045(self) -> None:
        game = unique_card_play("PAN045")
        card = game.decks[0].cards["pan045"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])

    def test_card_PAN046(self) -> None:
        game = unique_card_play("PAN046")
        card = game.decks[0].cards["pan046"]
        self.assertEqual(card.base_power + 20, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        self.assertEqual(zeros((7), dtype=int), card.buff["power"])
        self.assertEqual(zeros((7), dtype=int), card.buff["cost"])
