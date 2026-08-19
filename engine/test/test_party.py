"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.engine import Engine

# Python
from copy import deepcopy

"""___Tests_____________________________________________________________________________________"""


class TestParty(Assert):

    class TestParty_Modification(Assert):

        def test_modification_1(self, engine: Engine) -> None:
            player_deck = dummy_deck()
            player_deck.replace_carte("id0", engine.cartes["pca014"])
            opponent_deck = dummy_deck()
            init_party = engine.create_game(player_deck, opponent_deck, 100, 0, 0, 250)
            self.assertEqual(0, init_party.last_score[0])
            self.assertEqual(0, init_party.last_score[1])
            expected_party = deepcopy(init_party)
            _ = engine.play(init_party, ["pca014", None, None], [None, None, None])
            self.assertEqual(expected_party, init_party)

        def test_modification_2(self, engine: Engine) -> None:
            player_deck = Deck("test")
            player_deck.create_deck([engine.cartes[cid] for cid in deck_list_grodino])
            opponent_deck = dummy_deck()
            init_party = engine.create_game(player_deck, opponent_deck, 100, 0, 0, 250)
            expected_party = deepcopy(init_party)
            _ = engine.play(init_party, ["pan015", "pan035", "pan022"], [None, None, None])
            self.assertEqual(expected_party, init_party)

    class TestParty_CheckPlay(Assert):

        def test_check_play_1(self, engine: Engine) -> None:
            player_deck = dummy_deck()
            set_deck_cost(player_deck, 10)
            opponent_deck = dummy_deck()
            party = engine.create_game(player_deck, opponent_deck, 20, 0, 0, 250)
            # Play 1
            play = ["id0", "id1", None]
            self.assertEqual(True, party.check_play(play, 0))
            # Play 2
            play = ["id0", "id5", None]
            self.assertEqual(False, party.check_play(play, 0))
            # Play 3
            play = [None, None, None]
            self.assertEqual(True, party.check_play(play, 0))
            # Play 4
            play = ["id0", "id1", "id2"]
            self.assertEqual(False, party.check_play(play, 0))

        def test_check_play_2(self, engine: Engine) -> None:
            player_deck = dummy_deck()
            set_deck_cost(player_deck, 10)
            buff_array = get_buff_array(2, 1000)
            player_deck.cartes["id0"].buff["cost"] = buff_array
            buff_array = get_buff_array(1, 1)
            player_deck.cartes["id1"].buff["lock"] = buff_array
            opponent_deck = dummy_deck()
            party = engine.create_game(player_deck, opponent_deck, 20, 0, 0, 250)
            # Play 1
            play = ["id0", None, None]
            self.assertEqual(False, party.check_play(play, 0))
            # Play 2
            play = [None, "id1", None]
            self.assertEqual(False, party.check_play(play, 0))

    class TestParty_GetDeckPower(Assert):

        def test_get_deck_power_1(self, engine: Engine) -> None:
            player_deck = Deck("test")
            player_deck.create_deck([engine.cartes[cid] for cid in deck_list_grodino])
            expected = sum([carte.base_power for carte in player_deck.cartes.values()])
            opponent_deck = dummy_deck()
            party = engine.create_game(player_deck, opponent_deck, 100, 0, 0, 250)
            result = party.get_deck_power(0)
            self.assertEqual(expected, result)
