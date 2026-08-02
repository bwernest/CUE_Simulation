"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

"""___Tests_____________________________________________________________________________________"""


class TestCarteMultiplePlays(Assert):

    def test_carte_PAN063_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id5", engine.cartes["pan063"])
        opponent_deck = dummy_deck()
        set_deck_power(opponent_deck, 100)
        game = multiple_turns_play(
            player_plays=[["id0", None, None], ["pan063", None, None]],
            opponent_plays=[["id1", "id2", "id0"], ["id4", "id7", "id5"]],
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        carte = game.decks[0].cartes["pan063"]
        self.assertEqual(100 * 3, game.score[0, 0, 1])
        self.assertEqual(100 * 3, game.score[0, 1, 1])
        self.assertEqual(carte.base_power + 40, game.score[0, 1, 0])

    def test_carte_PHU013(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id4", engine.cartes["phu013"])
        game = multiple_turns_play(
            player_plays=[[None, None, None], ["phu013", None, None]],
            opponent_plays=[[None, None, None], [None, None, None]],
            player_deck=player_deck,
        )
        carte = game.decks[0].cartes["phu013"]
        self.assertEqual(carte.base_power + 9 * 2, game.score[0, 1, 0])
        self.assertEqual(100 - carte.base_cost, game.energy[0])
        expected_buff_array = get_buff_array(0, 9 * 2)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PIC023(self, engine: Engine) -> None:
        player_deck = collection_deck("Ice Age")
        player_deck.replace_carte("id4", engine.cartes["pic023"])
        game = multiple_turns_play(
            player_plays=[["id0", "id3", "id1"], ["id2", "pic023", "id5"]],
            opponent_plays=[[None, None, None], [None, None, None]],
            player_deck=player_deck,
        )
        carte = game.decks[0].cartes["pic023"]
        self.assertEqual(carte.base_power + 3 * 10, game.score[0, 1, 0])
        self.assertEqual(100 - carte.base_cost, game.energy[0])
        expected_buff_array = get_buff_array(0, 3 * 10)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PFF038_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["lmc033"])
        player_deck.replace_carte("id5", engine.cartes["pff038"])
        game = multiple_turns_play(
            player_plays=[["lmc033", None, None], [None, None, "pff038"]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        carteP = game.decks[0].cartes["lmc033"]
        carteD = game.decks[0].cartes["pff038"]
        self.assertEqual(carteP.base_power, game.score[0, 0, 0])
        self.assertEqual(carteD.base_power + 17, game.score[0, 1, 0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carteD.buff["power"])

    def test_carte_PFF038_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["lmc033"])
        player_deck.replace_carte("id4", engine.cartes["pff038"])
        game = multiple_turns_play(
            player_plays=[["lmc033", None, None], [None, None, "pff038"]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        carteP = game.decks[0].cartes["lmc033"]
        carteD = game.decks[0].cartes["pff038"]
        self.assertEqual(carteP.base_power, game.score[0, 0, 0])
        self.assertEqual(carteD.base_power, game.score[0, 1, 0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carteD.buff["power"])

    def test_carte_PFF038_unused(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["lmc033"])
        player_deck.replace_carte("id5", engine.cartes["pff038"])
        game = multiple_turns_play(
            player_plays=[["lmc033", None, None], [None, None, None]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        carteP = game.decks[0].cartes["lmc033"]
        carteD = game.decks[0].cartes["pff038"]
        self.assertEqual(carteP.base_power, game.score[0, 0, 0])
        self.assertEqual(0, game.score[0, 1, 0])
        expected_buff_array = get_buff_array(1, 17)
        self.assertEqual(expected_buff_array, carteD.buff["power"])

    def test_carte_PFF023_after(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["acph003"])
        player_deck.replace_carte("id3", engine.cartes["pff023"])
        game = multiple_turns_play(
            player_plays=[["acph003", None, None], ["pff023", None, None]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        carteP = game.decks[0].cartes["acph003"]
        carteF = game.decks[0].cartes["pff023"]
        self.assertEqual(carteP.base_power, game.score[0, 0, 0])
        self.assertEqual(carteF.base_power, game.score[0, 1, 0])
        expected_buff_array = get_buff_array(1, 18 + 16)
        self.assertEqual(expected_buff_array, carteP.buff["power"])

    def test_carte_PFF023_before(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["acph003"])
        player_deck.replace_carte("id3", engine.cartes["pff023"])
        game = multiple_turns_play(
            player_plays=[["pff023", None, None]],
            opponent_plays=[[None] * 3],
            player_deck=player_deck,
        )
        carteF = game.decks[0].cartes["pff023"]
        carteP = game.decks[0].cartes["acph003"]
        self.assertEqual(carteF.base_power, game.score[0, 0, 0])
        expected_buff_array = get_buff_array(1, 18)
        self.assertEqual(expected_buff_array, carteP.buff["power"])

    def test_carte_PHE028(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["lre042"])
        player_deck.replace_carte("id3", engine.cartes["phe028"])
        game = multiple_turns_play(
            player_plays=[["lre042", None, None], [None, "phe028", None]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        carteT = game.decks[0].cartes["lre042"]
        carteL = game.decks[0].cartes["phe028"]
        self.assertEqual(carteT.base_power, game.score[0, 0, 0])
        expected_buff_array = get_buff_array(4, 2)
        self.assertEqual(expected_buff_array, game.resource_per_turn["energy"][0])
        self.assertEqual(100 - carteT.base_cost - carteL.base_cost + 2, game.energy[0])

    def test_carte_PHE014(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["phe014"])
        opponent_deck = dummy_deck()
        set_deck_power(opponent_deck, 100)
        game = multiple_turns_play(
            player_plays=[[None, None, None], [None, "phe014", None]],
            opponent_plays=[["id0", "id1", "id2"], [None] * 3],
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        carte = game.decks[0].cartes["phe014"]
        self.assertEqual(carte.base_power + 49, game.score[0, 1, 0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])
