"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

"""___Tests_____________________________________________________________________________________"""


class TestTurnSinglePlay(Assert):

    def test_card_PMO030_true(self, engine: Engine) -> None:
        player_deck = collection_deck("Monsters of The Deep")
        player_deck.replace_card("id0", engine.cards["pmo030"])
        game = unique_turn_play(["id1", "pmo030", "id2"], [None] * 3, player_deck)
        card = game.decks[0].cards["pmo030"]
        self.assertEqual(card.base_power + 15 * 3, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PMO030_false(self, engine: Engine) -> None:
        player_deck = album_deck("Paleontology")
        player_deck.replace_card("id0", engine.cards["pmo030"])
        game = unique_turn_play(["id1", "pmo030", None], [None] * 3, player_deck)
        card = game.decks[0].cards["pmo030"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PCA045_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["pca045"])
        player_deck.replace_card("id1", engine.cards["pca013"])
        game = unique_turn_play(["pca013", "pca045", None], [None] * 3, player_deck)

        card_45 = game.decks[0].cards["pca045"]
        card_13 = game.decks[0].cards["pca013"]
        self.assertEqual(card_45.base_power + card_13.base_power + 15 * 2 + 6, game.score[0, 0, 0])
        self.assertEqual(100 - card_45.base_cost - card_13.base_cost, game.energy[0])

        expected_buff_array = get_buff_array(3, 15)
        self.assertEqual(expected_buff_array, card_45.buff["power"])
        self.assertEqual(expected_buff_array, card_13.buff["power"])

        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, game.resource_per_turn["power"][0])

    def test_card_PCA045_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["pca045"])
        player_deck.replace_card("id1", engine.cards["pca013"])
        game = unique_turn_play(["pca013", None, "pca045"], [None] * 3, player_deck)

        card_45 = game.decks[0].cards["pca045"]
        card_13 = game.decks[0].cards["pca013"]
        self.assertEqual(card_45.base_power + card_13.base_power + 6, game.score[0, 0, 0])
        self.assertEqual(100 - card_45.base_cost - card_13.base_cost, game.energy[0])

        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card_45.buff["power"])
        self.assertEqual(expected_buff_array, card_13.buff["power"])
        self.assertEqual(expected_buff_array, game.resource_per_turn["power"][0])

    def test_card_PMO040_false(self, engine: Engine) -> None:
        player_deck = album_deck("Paleontology")
        player_deck.replace_card("id0", engine.cards["pmo040"])
        game = unique_turn_play(["pmo040", "id1", "id2"], [None] * 3, player_deck)
        card = game.decks[0].cards["pmo040"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PMO040_true(self, engine: Engine) -> None:
        player_deck = album_deck("Science")
        player_deck.replace_card("id0", engine.cards["pmo040"])
        game = unique_turn_play(["pmo040", "id1", "id2"], [None] * 3, player_deck)
        card = game.decks[0].cards["pmo040"]
        self.assertEqual(card.base_power + 20, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array(2, 20)
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PAN058_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_card("id0", engine.cards["pan058"])
        player_deck.replace_card("id1", engine.cards["sbb001"])
        game = unique_turn_play(["sbb001", "pan058", None], [None] * 3, player_deck)
        cardP = game.decks[0].cards["pan058"]
        cardS = game.decks[0].cards["sbb001"]
        self.assertEqual(cardP.base_power + 9 + 60 + cardS.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - cardP.base_cost + 1 - cardS.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, cardP.buff["power"])
        expected_buff_array = get_buff_array(2, -1)
        self.assertEqual(expected_buff_array, cardP.buff["cost"])

    def test_card_PCA027(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        set_deck_cost(player_deck, 10)
        player_deck.replace_card("id4", engine.cards["pca027"])
        opponent_deck = dummy_deck()
        set_deck_cost(opponent_deck, 10)
        game = unique_turn_play(["id0", "id1", "id3"], ["id4", "id2", "id1"], player_deck, opponent_deck)
        card = game.decks[0].cards["pca027"]
        self.assertEqual(100 - (10 + 1) * 3 + 3, game.energy[0])
        self.assertEqual(100 - (10 + 1) * 3, game.energy[1])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["cost"])

    def test_card_POM020(self, engine: Engine) -> None:
        player_deck = album_deck("Paleontology")
        player_deck.replace_card("id0", engine.cards["pom020"])
        opponent_deck = dummy_deck()
        set_deck_power(opponent_deck, 100)
        game = unique_turn_play(["pom020", None, None], ["id4", "id2", "id1"], player_deck, opponent_deck)
        cardA = game.decks[0].cards["pom020"]
        card1 = game.decks[0].cards["id1"]
        self.assertEqual(cardA.base_power, game.score[0, 0, 0])
        self.assertEqual(3 * 100, game.score[0, 0, 1])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, cardA.buff["power"])
        expected_buff_array = get_buff_array(3, 20)
        self.assertEqual(expected_buff_array, card1.buff["power"])
        expected_buff_array = get_buff_array(2, 35)
        self.assertEqual(expected_buff_array, game.resource_per_turn["power"][0])
