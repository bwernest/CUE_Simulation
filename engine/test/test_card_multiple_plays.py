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
        party = multiple_turns_play(
            player_plays=[["id0", None, None], ["pan063", None, None]],
            opponent_plays=[["id1", "id2", "id0"], ["id4", "id7", "id5"]],
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        carte = party.decks[0].cartes["pan063"]
        self.assertEqual(100 * 3, party.score[0, 0, 1])
        self.assertEqual(100 * 3, party.score[0, 1, 1])
        self.assertEqual(carte.base_power + 40, party.score[0, 1, 0])

    def test_carte_PHU013(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id4", engine.cartes["phu013"])
        party = multiple_turns_play(
            player_plays=[[None, None, None], ["phu013", None, None]],
            opponent_plays=[[None, None, None], [None, None, None]],
            player_deck=player_deck,
        )
        carte = party.decks[0].cartes["phu013"]
        self.assertEqual(carte.base_power + 9 * 2, party.score[0, 1, 0])
        self.assertEqual(100 - carte.base_cost, party.energy[0])
        expected_buff_array = get_buff_array(0, 9 * 2)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PIC023(self, engine: Engine) -> None:
        player_deck = collection_deck("Ice Age")
        player_deck.replace_carte("id4", engine.cartes["pic023"])
        party = multiple_turns_play(
            player_plays=[["id0", "id3", "id1"], ["id2", "pic023", "id5"]],
            opponent_plays=[[None, None, None], [None, None, None]],
            player_deck=player_deck,
        )
        carte = party.decks[0].cartes["pic023"]
        self.assertEqual(carte.base_power + 3 * 10, party.score[0, 1, 0])
        self.assertEqual(100 - carte.base_cost, party.energy[0])
        expected_buff_array = get_buff_array(0, 3 * 10)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PFF038_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["lmc033"])
        player_deck.replace_carte("id5", engine.cartes["pff038"])
        party = multiple_turns_play(
            player_plays=[["lmc033", None, None], [None, None, "pff038"]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        carteP = party.decks[0].cartes["lmc033"]
        carteD = party.decks[0].cartes["pff038"]
        self.assertEqual(carteP.base_power, party.score[0, 0, 0])
        self.assertEqual(carteD.base_power + 17, party.score[0, 1, 0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carteD.buff["power"])

    def test_carte_PFF038_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["lmc033"])
        player_deck.replace_carte("id4", engine.cartes["pff038"])
        party = multiple_turns_play(
            player_plays=[["lmc033", None, None], [None, None, "pff038"]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        carteP = party.decks[0].cartes["lmc033"]
        carteD = party.decks[0].cartes["pff038"]
        self.assertEqual(carteP.base_power, party.score[0, 0, 0])
        self.assertEqual(carteD.base_power, party.score[0, 1, 0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carteD.buff["power"])

    def test_carte_PFF038_unused(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["lmc033"])
        player_deck.replace_carte("id5", engine.cartes["pff038"])
        party = multiple_turns_play(
            player_plays=[["lmc033", None, None], [None, None, None]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        carteP = party.decks[0].cartes["lmc033"]
        carteD = party.decks[0].cartes["pff038"]
        self.assertEqual(carteP.base_power, party.score[0, 0, 0])
        self.assertEqual(0, party.score[0, 1, 0])
        expected_buff_array = get_buff_array(1, 17)
        self.assertEqual(expected_buff_array, carteD.buff["power"])

    def test_carte_PFF023_after(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["acph003"])
        player_deck.replace_carte("id3", engine.cartes["pff023"])
        party = multiple_turns_play(
            player_plays=[["acph003", None, None], ["pff023", None, None]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        carteP = party.decks[0].cartes["acph003"]
        carteF = party.decks[0].cartes["pff023"]
        self.assertEqual(carteP.base_power, party.score[0, 0, 0])
        self.assertEqual(carteF.base_power, party.score[0, 1, 0])
        expected_buff_array = get_buff_array(1, 18 + 16)
        self.assertEqual(expected_buff_array, carteP.buff["power"])

    def test_carte_PFF023_before(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["acph003"])
        player_deck.replace_carte("id3", engine.cartes["pff023"])
        party = multiple_turns_play(
            player_plays=[["pff023", None, None]],
            opponent_plays=[[None] * 3],
            player_deck=player_deck,
        )
        carteF = party.decks[0].cartes["pff023"]
        carteP = party.decks[0].cartes["acph003"]
        self.assertEqual(carteF.base_power, party.score[0, 0, 0])
        expected_buff_array = get_buff_array(1, 18)
        self.assertEqual(expected_buff_array, carteP.buff["power"])

    def test_carte_PHE028(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["lre042"])
        player_deck.replace_carte("id3", engine.cartes["phe028"])
        party = multiple_turns_play(
            player_plays=[["lre042", None, None], [None, "phe028", None]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        carteT = party.decks[0].cartes["lre042"]
        carteL = party.decks[0].cartes["phe028"]
        self.assertEqual(carteT.base_power, party.score[0, 0, 0])
        expected_buff_array = get_buff_array(4, 2)
        self.assertEqual(expected_buff_array, party.resource_per_turn["energy"][0])
        self.assertEqual(100 - carteT.base_cost - carteL.base_cost + 2, party.energy[0])

    def test_carte_PHE014(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["phe014"])
        opponent_deck = dummy_deck()
        set_deck_power(opponent_deck, 100)
        party = multiple_turns_play(
            player_plays=[[None, None, None], [None, "phe014", None]],
            opponent_plays=[["id0", "id1", "id2"], [None] * 3],
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        carte = party.decks[0].cartes["phe014"]
        self.assertEqual(carte.base_power + 49, party.score[0, 1, 0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PFF026_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        set_deck_power(player_deck, 100)
        player_deck.replace_carte("id1", engine.cartes["pff026"])
        party = multiple_turns_play(
            player_plays=[[None, None, "id0"], [None] * 3, [None] * 3, [None, "pff026", None]],
            opponent_plays=[[None] * 3, [None] * 3, [None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        expected_buff_array = get_buff_array(4, 5)
        result = party.resource_per_turn["energy"][0]
        self.assertEqual(expected_buff_array, result)

    def test_carte_PFF026_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id1", engine.cartes["pff026"])
        set_deck_power(player_deck, 100)
        opponent_deck = dummy_deck()
        set_deck_power(opponent_deck, 100)
        party = multiple_turns_play(
            player_plays=[[None, None, "id0"], [None] * 3, [None] * 3, [None, "pff026", None]],
            opponent_plays=[[None] * 3, [None] * 3, [None] * 3, [None, "id0", None]],
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        expected_buff_array = get_buff_array()
        result = party.resource_per_turn["energy"][0]
        self.assertEqual(expected_buff_array, result)

    def test_carte_PGB013_true(self, engine: Engine) -> None:
        player_deck = collection_deck("Fearsome Flyers")
        player_deck.replace_carte("id0", engine.cartes["pgb013"])
        party = multiple_turns_play(
            player_plays=[["id1", "id2", "id3"], ["id4", "id5", "pgb013"]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        expected_buff_array = get_buff_array(1, 20)
        for id in range(1, 4):
            result = party.decks[0].cartes[f"id{id}"].buff["power"]
            self.assertEqual(expected_buff_array, result)
        expected_buff_array = get_buff_array()
        for id in range(4, 18):
            result = party.decks[0].cartes[f"id{id}"].buff["power"]
            self.assertEqual(expected_buff_array, result)

    def test_carte_PGB013_true_2_games(self, engine: Engine) -> None:

        # ___Game_1___
        player_deck = collection_deck("Fearsome Flyers")
        player_deck.replace_carte("id0", engine.cartes["pgb013"])
        party = multiple_turns_play(
            player_plays=[["id1", "id2", "id3"], ["id4", "id5", "pgb013"]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        expected_buff_array = get_buff_array(1, 20)
        for id in range(1, 4):
            result = party.decks[0].cartes[f"id{id}"].buff["power"]
            self.assertEqual(expected_buff_array, result)
        expected_buff_array = get_buff_array()
        for id in range(4, 18):
            result = party.decks[0].cartes[f"id{id}"].buff["power"]
            self.assertEqual(expected_buff_array, result)

        # ___Game_2___
        player_deck = collection_deck("Fearsome Flyers")
        player_deck.replace_carte("id0", engine.cartes["pgb013"])
        party = multiple_turns_play(
            player_plays=[["id1", "id2", "id3"], ["id4", "id5", "pgb013"]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck,
        )
        expected_buff_array = get_buff_array(1, 20)
        for id in range(1, 4):
            result = party.decks[0].cartes[f"id{id}"].buff["power"]
            self.assertEqual(expected_buff_array, result)
        expected_buff_array = get_buff_array()
        for id in range(4, 18):
            result = party.decks[0].cartes[f"id{id}"].buff["power"]
            self.assertEqual(expected_buff_array, result)
