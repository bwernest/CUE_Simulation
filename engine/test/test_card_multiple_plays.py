"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

# Python
from numpy import zeros

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

    def test_card_PHU013(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id4", engine.cards["phu013"])
        game = multiple_turns_play(
            player_plays=[[None, None, None], ["phu013", None, None]],
            opponent_plays=[[None, None, None], [None, None, None]],
            player_deck=player_deck,
        )
        card = game.decks[0].cards["phu013"]
        self.assertEqual(card.base_power + 9 * 2, game.score[0, 1, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = zeros((game.buff_array_len), dtype=int)
        expected_buff_array[0] += 9 * 2
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PIC023(self, engine: Engine) -> None:
        player_deck = collection_deck("Ice Age")
        player_deck.replace_card("id4", engine.cards["pic023"])
        game = multiple_turns_play(
            player_plays=[["id0", "id3", "id1"], ["id2", "pic023", "id5"]],
            opponent_plays=[[None, None, None], [None, None, None]],
            player_deck=player_deck,
        )
        card = game.decks[0].cards["pic023"]
        self.assertEqual(card.base_power + 3 * 10, game.score[0, 1, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = zeros((game.buff_array_len), dtype=int)
        expected_buff_array[0] += 3 * 10
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PFF038_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["lmc033"])
        player_deck.replace_card("id5", engine.cards["pff038"])
        game = multiple_turns_play(
            [["lmc033", None, None], [None, None, "pff038"]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck
        )
        cardP = game.decks[0].cards["lmc033"]
        cardD = game.decks[0].cards["pff038"]
        self.assertEqual(cardP.base_power, game.score[0, 0, 0])
        self.assertEqual(cardD.base_power + 17, game.score[0, 1, 0])
        self.assertEqual(zeros((game.buff_array_len), dtype=int), cardD.buff["power"])

    def test_card_PFF038_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["lmc033"])
        player_deck.replace_card("id4", engine.cards["pff038"])
        game = multiple_turns_play(
            [["lmc033", None, None], [None, None, "pff038"]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck
        )
        cardP = game.decks[0].cards["lmc033"]
        cardD = game.decks[0].cards["pff038"]
        self.assertEqual(cardP.base_power, game.score[0, 0, 0])
        self.assertEqual(cardD.base_power, game.score[0, 1, 0])
        self.assertEqual(zeros((game.buff_array_len), dtype=int), cardD.buff["power"])

    def test_card_PFF038_unused(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["lmc033"])
        player_deck.replace_card("id5", engine.cards["pff038"])
        game = multiple_turns_play(
            [["lmc033", None, None], [None, None, None]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck
        )
        cardP = game.decks[0].cards["lmc033"]
        cardD = game.decks[0].cards["pff038"]
        self.assertEqual(cardP.base_power, game.score[0, 0, 0])
        self.assertEqual(0, game.score[0, 1, 0])
        expected_buff_array = zeros((game.buff_array_len), dtype=int)
        expected_buff_array[1] += 17
        self.assertEqual(expected_buff_array, cardD.buff["power"])

    def test_card_PFF023_after(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["acph003"])
        player_deck.replace_card("id3", engine.cards["pff023"])
        game = multiple_turns_play(
            [["acph003", None, None], ["pff023", None, None]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck
        )
        cardP = game.decks[0].cards["acph003"]
        cardF = game.decks[0].cards["pff023"]
        self.assertEqual(cardP.base_power, game.score[0, 0, 0])
        self.assertEqual(cardF.base_power, game.score[0, 1, 0])
        expected_buff_array = zeros((game.buff_array_len), dtype=int)
        expected_buff_array[1] += 18 + 16
        self.assertEqual(expected_buff_array, cardP.buff["power"])

    def test_card_PFF023_before(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["acph003"])
        player_deck.replace_card("id3", engine.cards["pff023"])
        game = multiple_turns_play(
            [["pff023", None, None]],
            opponent_plays=[[None] * 3],
            player_deck=player_deck
        )
        cardF = game.decks[0].cards["pff023"]
        cardP = game.decks[0].cards["acph003"]
        self.assertEqual(cardF.base_power, game.score[0, 0, 0])
        expected_buff_array = zeros((game.buff_array_len), dtype=int)
        expected_buff_array[1] += 18
        self.assertEqual(expected_buff_array, cardP.buff["power"])

    def test_card_PHE028(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["lre042"])
        player_deck.replace_card("id3", engine.cards["phe028"])
        game = multiple_turns_play(
            [["lre042", None, None], [None, "phe028", None]],
            opponent_plays=[[None] * 3, [None] * 3],
            player_deck=player_deck
        )
        cardT = game.decks[0].cards["lre042"]
        cardL = game.decks[0].cards["phe028"]
        self.assertEqual(cardT.base_power, game.score[0, 0, 0])
        expected_buff_array = zeros((game.buff_array_len), dtype=int)
        expected_buff_array[4] += 2
        self.assertEqual(expected_buff_array, game.resource_per_turn["energy"][0])
        self.assertEqual(100 - cardT.base_cost - cardL.base_cost + 2, game.energy[0])
