"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

# Python
from numpy import array, sum, zeros

"""___Tests_____________________________________________________________________________________"""


class TestCardMultiplePlays(Assert):

    def test_card_PAN063_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id5", engine.cards["pan063"])
        opponent_deck = dummy_deck()
        set_deck_power(opponent_deck, 100)
        game = multiple_turns_play(
            player_plays=[["id0", None, None], ["pan063", None, None]],
            opponent_plays=[["id1", "id2", "id0"], ["id4", "id7", "id5"]],
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        card = game.decks[0].cards["pan063"]
        self.assertEqual(100 * 3, game.score[0, 0, 1])
        self.assertEqual(100 * 3, game.score[0, 1, 1])
        self.assertEqual(card.base_power + 40, game.score[0, 1, 0])
