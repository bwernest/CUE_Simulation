"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.engine import Engine

# Python
from copy import deepcopy

"""___Tests_____________________________________________________________________________________"""


class TestParty(Assert):

    def test_modification_1(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["pca014"])
        opponent_deck = dummy_deck()
        inti_party = engine.create_game(player_deck, opponent_deck, 100, 0, 0, 250)
        expected_party = deepcopy(inti_party)
        _ = engine.play(inti_party, ["pca014", None, None], [None, None, None])
        self.assertEqual(expected_party, inti_party)

    def test_modification_2(self, engine: Engine) -> None:
        player_deck = Deck("test")
        player_deck.create_deck([engine.cartes[cid] for cid in deck_list_grodino])
        opponent_deck = dummy_deck()
        inti_party = engine.create_game(player_deck, opponent_deck, 100, 0, 0, 250)
        expected_party = deepcopy(inti_party)
        _ = engine.play(inti_party, ["pan015", "pan035", "pan022"], [None, None, None])
        self.assertEqual(expected_party, inti_party)
