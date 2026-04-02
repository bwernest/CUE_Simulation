"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

# Python
from numpy import array, sum

"""___Tests_____________________________________________________________________________________"""


class TestCardSinglePlay(Assert):

    def test_card_MYPA001(self) -> None:
        game = unique_card_play("MYPA001")
        card = game.decks[0].cards["mypa001"]
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, game.resource_per_turn["energy"][0])
        self.assertEqual(card.base_power + 77, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        self.assertEqual({
            "album": {"paleontology": 1, "test_album": 17},
            "collection": {"paleontology mythic cards": 1, "test_collection": 17}
        }, game.stats[0])

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
        total_hand_buff = int(sum([sum(game.decks[0].cards[card_id].buff["power"]) for card_id in game.decks[0].hand]))
        self.assertIn(total_hand_buff, [0, 46, 46 * 2])
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
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])
        self.assertEqual(expected_buff_array, card.buff["cost"])

    def test_card_PAN022(self) -> None:
        game = unique_card_play("PAN022")
        card = game.decks[0].cards["pan022"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, game.resource_per_turn["power"][0])

        game = unique_card_play("PAN022", album_deck("Paleontology"))
        card = game.decks[0].cards["pan022"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array(3, 25)
        self.assertEqual(expected_buff_array, game.resource_per_turn["power"][0])

    def test_card_PCA023(self) -> None:
        game = unique_card_play("PCA023", album_deck("Paleontology"))
        card = game.decks[0].cards["pca023"]
        self.assertEqual(card.base_power + 35, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array(3, 35)
        self.assertEqual(expected_buff_array, card.buff["power"])
        self.assertEqual(expected_buff_array, game.decks[0].cards["id1"].buff["power"])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, game.decks[1].cards["id1"].buff["power"])

    def test_card_PIC008(self) -> None:
        deck = album_deck("Paleontology")
        for card_id in range(10):
            deck.cards[f"id{card_id}"].base_cost = 10
        for card_id in range(0, 3):
            deck.cards[f"id{card_id}"].rarity = "rare"
        for card_id in range(3, 6):
            deck.cards[f"id{card_id}"].rarity = "epic"
        for card_id in range(6, 9):
            deck.cards[f"id{card_id}"].rarity = "legendary"

        game = unique_card_play("PIC008", deck)
        card = game.decks[0].cards["pic008"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost + 1, game.energy[0])

        for card_id in range(1, 3):
            self.assertEqual(-1, deck.cards[f"id{card_id}"].buff["cost"][0])
        for card_id in range(3, 6):
            self.assertEqual(-1, deck.cards[f"id{card_id}"].buff["cost"][0])
        for card_id in range(6, 9):
            self.assertEqual(0, deck.cards[f"id{card_id}"].buff["cost"][0])

    def test_card_PAN058(self) -> None:
        game = unique_card_play("PAN058")
        card = game.decks[0].cards["pan058"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost + 1, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])
        expected_buff_array = get_buff_array(2, -1)
        self.assertEqual(expected_buff_array, card.buff["cost"])

    def test_card_PMO030(self) -> None:
        game = unique_card_play("PMO030")
        card = game.decks[0].cards["pmo030"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PMO045_false(self) -> None:
        game = unique_card_play("PMO045")
        card = game.decks[0].cards["pmo045"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PMO045_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        for card_id, card in player_deck.cards.items():
            card.album = card_id    # L'histoire d'avoir des albums différents
        game = unique_card_play("PMO045", player_deck)
        card = game.decks[0].cards["pmo045"]
        self.assertEqual(card.base_power + 20, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array(0, 10)
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PMO040(self) -> None:
        game = unique_card_play("PMO040")
        card = game.decks[0].cards["pmo040"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PAN063(self) -> None:
        game = unique_card_play("PAN063")
        card = game.decks[0].cards["pan063"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])

    def test_card_PHU013(self) -> None:
        game = unique_card_play("PHU013")
        card = game.decks[0].cards["phu013"]
        self.assertEqual(card.base_power + 9, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array(0, 9)
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PIC023(self) -> None:
        game = unique_card_play("PIC023")
        card = game.decks[0].cards["pic023"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PCA036(self) -> None:
        player_deck = dummy_deck()
        opponent_deck = dummy_deck()
        set_deck_power(player_deck, 100)
        set_deck_power(opponent_deck, 100)
        game = unique_card_play("PCA036", player_deck=player_deck, opponent_deck=opponent_deck)
        card = game.decks[0].cards["pca036"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])

        expected_buff_array = get_buff_array(2, -50)
        for player in range(2):
            for card_id in game.decks[player].remaining:
                self.assertEqual(expected_buff_array, game.decks[player].cards[card_id].buff["power"])

    def test_card_PFF038(self) -> None:
        game = unique_card_play("PFF038")
        card = game.decks[0].cards["pff038"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PFF023(self) -> None:
        game = unique_card_play("PFF023")
        card = game.decks[0].cards["pff023"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])

    def test_card_PHE028(self) -> None:
        game = unique_card_play("PHE028")
        card = game.decks[0].cards["phe028"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, game.resource_per_turn["energy"][0])

    def test_card_PCA003(self) -> None:
        game = unique_card_play("PCA003")
        card = game.decks[0].cards["pca003"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(-12, game.score[0, 0, 1])
        expected_buff_array = get_buff_array(3, -12)
        self.assertEqual(expected_buff_array, game.resource_per_turn["power"][1])

    def test_card_PLB006_1(self) -> None:
        player_deck = album_deck("Paleontology")
        game = unique_card_play("PLB006", player_deck=player_deck)
        card = game.decks[0].cards["plb006"]
        self.assertEqual(card.base_power - 10, game.score[0, 0, 0])
        expected_buff_array = get_buff_array(0, -10)
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PLB006_2(self) -> None:
        player_deck = album_deck("Science")
        game = unique_card_play("PLB006", player_deck=player_deck)
        card = game.decks[0].cards["plb006"]
        self.assertEqual(card.base_power - 20, game.score[0, 0, 0])
        expected_buff_array = get_buff_array(0, -20)
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PCA027(self) -> None:
        game = unique_card_play("PCA027")
        card = game.decks[0].cards["pca027"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost - 1 + 3, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["cost"])

    def test_card_POM020(self) -> None:
        game = unique_card_play("POM020")
        card = game.decks[0].cards["pom020"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, card.buff["power"])

    def test_card_PHE014(self) -> None:
        game = unique_card_play("PHE014")
        card = game.decks[0].cards["phe014"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])

    def test_card_PHE024(self) -> None:
        game = unique_card_play("PHE024")
        card = game.decks[0].cards["phe024"]
        self.assertEqual(card.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - card.base_cost, game.energy[0])
