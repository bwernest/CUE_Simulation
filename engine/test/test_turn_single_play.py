"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

# Python
from numpy import array, sum, zeros

"""___Tests_____________________________________________________________________________________"""


class TestTurnSinglePlay(Assert):

    def test_card_PMO030_true(self, engine: Engine) -> None:
        player_deck = collection_deck("Monsters of The Deep")
        player_deck.replace_card("id0", engine.cards["pmo030"])
        game = unique_turn_play(["id1", "pmo030", "id2"], [None]*3, player_deck)
        card = game.decks[0].cards["pmo030"]
        self.assertEqual(card.base_power + 15 * 3, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        self.assertEqual(zeros((game.buff_array_len), dtype=int), card.buff["power"])

    def test_card_PMO030_false(self, engine: Engine) -> None:
        player_deck = album_deck("Paleontology")
        player_deck.replace_card("id0", engine.cards["pmo030"])
        game = unique_turn_play(["id1", "pmo030", None], [None]*3, player_deck)
        card = game.decks[0].cards["pmo030"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        self.assertEqual(zeros((game.buff_array_len), dtype=int), card.buff["power"])

    def test_card_PCA045_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["pca045"])
        player_deck.replace_card("id1", engine.cards["pca013"])
        game = unique_turn_play(["pca013", "pca045", None], [None]*3, player_deck)

        card_45 = game.decks[0].cards["pca045"]
        card_13 = game.decks[0].cards["pca013"]
        self.assertEqual(card_45.base_power + card_13.base_power + 15*2+6, game.score[0, 0, 0])
        self.assertEqual(100 - card_45.base_cost-card_13.base_cost, game.energy[0])

        expected_card_buff_array = zeros((game.buff_array_len), dtype=int)
        expected_card_buff_array[3] += 15
        self.assertEqual(expected_card_buff_array, card_45.buff["power"])
        self.assertEqual(expected_card_buff_array, card_13.buff["power"])

        expected_player_buff_array = zeros((game.buff_array_len), dtype=int)
        self.assertEqual(expected_player_buff_array, game.resource_per_turn["power"][0])

    def test_card_PCA045_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["pca045"])
        player_deck.replace_card("id1", engine.cards["pca013"])
        game = unique_turn_play(["pca013", None, "pca045"], [None]*3, player_deck)

        card_45 = game.decks[0].cards["pca045"]
        card_13 = game.decks[0].cards["pca013"]
        self.assertEqual(card_45.base_power + card_13.base_power + 6, game.score[0, 0, 0])
        self.assertEqual(100 - card_45.base_cost-card_13.base_cost, game.energy[0])

        expected_card_buff_array = zeros((game.buff_array_len), dtype=int)
        self.assertEqual(expected_card_buff_array, card_45.buff["power"])
        self.assertEqual(expected_card_buff_array, card_13.buff["power"])

        expected_player_buff_array = zeros((game.buff_array_len), dtype=int)
        self.assertEqual(expected_player_buff_array, game.resource_per_turn["power"][0])
