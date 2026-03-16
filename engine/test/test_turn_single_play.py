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
