"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

# Python
from random import seed
from numpy import array

"""___Tests_____________________________________________________________________________________"""


class TestTurnSinglePlay(Assert):

    def test_carte_PMO030_true(self, engine: Engine) -> None:
        player_deck = collection_deck("monsters of the deep")
        player_deck.replace_carte("id0", engine.cartes["pmo030"])
        party = unique_turn_play(["id1", "pmo030", "id2"], [None] * 3, player_deck)
        carte = party.decks[0].cartes["pmo030"]
        self.assertEqual(carte.base_power + 15 * 3, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PMO030_false(self, engine: Engine) -> None:
        player_deck = album_deck("paleontology")
        player_deck.replace_carte("id0", engine.cartes["pmo030"])
        party = unique_turn_play(["id1", "pmo030", None], [None] * 3, player_deck)
        carte = party.decks[0].cartes["pmo030"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PCA045_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["pca045"])
        player_deck.replace_carte("id1", engine.cartes["pca013"])
        party = unique_turn_play(["pca013", "pca045", None], [None] * 3, player_deck)

        carte_45 = party.decks[0].cartes["pca045"]
        carte_13 = party.decks[0].cartes["pca013"]
        self.assertEqual(carte_45.base_power + carte_13.base_power + 15 * 2 + 6, party.score[0, 0, 0])
        self.assertEqual(100 - carte_45.base_cost - carte_13.base_cost, party.energie[0])

        expected_buff_array = get_buff_array(3, 15)
        self.assertEqual(expected_buff_array, carte_45.buff["power"])
        self.assertEqual(expected_buff_array, carte_13.buff["power"])

        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, party.resource_per_turn["power"][0])

    def test_carte_PCA045_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["pca045"])
        player_deck.replace_carte("id1", engine.cartes["pca013"])
        party = unique_turn_play(["pca013", None, "pca045"], [None] * 3, player_deck)

        carte_45 = party.decks[0].cartes["pca045"]
        carte_13 = party.decks[0].cartes["pca013"]
        self.assertEqual(carte_45.base_power + carte_13.base_power + 6, party.score[0, 0, 0])
        self.assertEqual(100 - carte_45.base_cost - carte_13.base_cost, party.energie[0])

        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte_45.buff["power"])
        self.assertEqual(expected_buff_array, carte_13.buff["power"])
        self.assertEqual(expected_buff_array, party.resource_per_turn["power"][0])

    def test_carte_PMO040_false(self, engine: Engine) -> None:
        player_deck = album_deck("paleontology")
        player_deck.replace_carte("id0", engine.cartes["pmo040"])
        party = unique_turn_play(["pmo040", "id1", "id2"], [None] * 3, player_deck)
        carte = party.decks[0].cartes["pmo040"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PMO040_true(self, engine: Engine) -> None:
        player_deck = album_deck("science")
        player_deck.replace_carte("id0", engine.cartes["pmo040"])
        party = unique_turn_play(["pmo040", "id1", "id2"], [None] * 3, player_deck)
        carte = party.decks[0].cartes["pmo040"]
        self.assertEqual(carte.base_power + 20, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array(2, 20)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PAN058_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["pan058"])
        player_deck.replace_carte("id1", engine.cartes["sbb001"])
        party = unique_turn_play(["sbb001", "pan058", None], [None] * 3, player_deck)
        carteP = party.decks[0].cartes["pan058"]
        carteS = party.decks[0].cartes["sbb001"]
        self.assertEqual(carteP.base_power + 9 + 60 + carteS.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carteP.base_cost + 1 - carteS.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carteP.buff["power"])
        expected_buff_array = get_buff_array(2, -1)
        self.assertEqual(expected_buff_array, carteP.buff["cost"])

    def test_carte_PCA027(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        set_deck_cost(player_deck, 10)
        player_deck.replace_carte("id4", engine.cartes["pca027"])
        opponent_deck = dummy_deck()
        set_deck_cost(opponent_deck, 10)
        party = unique_turn_play(["id0", "id1", "id3"], ["id4", "id2", "id1"], player_deck, opponent_deck)
        carte = party.decks[0].cartes["pca027"]
        self.assertEqual(100 - (10 + 1) * 3 + 3, party.energie[0])
        self.assertEqual(100 - (10 + 1) * 3, party.energie[1])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["cost"])

    def test_carte_POM020(self, engine: Engine) -> None:
        player_deck = album_deck("paleontology")
        player_deck.replace_carte("id0", engine.cartes["pom020"])
        opponent_deck = dummy_deck()
        set_deck_power(opponent_deck, 100)
        party = unique_turn_play(["pom020", None, None], ["id4", "id2", "id1"], player_deck, opponent_deck)
        carteA = party.decks[0].cartes["pom020"]
        carte1 = party.decks[0].cartes["id1"]
        self.assertEqual(carteA.base_power, party.score[0, 0, 0])
        self.assertEqual(3 * 100, party.score[0, 0, 1])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carteA.buff["power"])
        expected_buff_array = get_buff_array(3, 20)
        self.assertEqual(expected_buff_array, carte1.buff["power"])
        expected_buff_array = get_buff_array(2, 35)
        self.assertEqual(expected_buff_array, party.resource_per_turn["power"][0])

    def test_carte_PHE024_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["phe014"])
        player_deck.replace_carte("id1", engine.cartes["phe024"])
        party = unique_turn_play(
            player_play=[None, "phe024", None],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        carte = party.decks[0].cartes["phe014"]
        expected_buff_array = get_buff_array(0, 49)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PHE024_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id5", engine.cartes["phe014"])
        player_deck.replace_carte("id1", engine.cartes["phe024"])
        party = unique_turn_play(
            player_play=[None, "phe024", None],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        carte = party.decks[0].cartes["phe014"]
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PCA033_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id1", engine.cartes["pca033"])
        party = unique_turn_play(
            player_play=[None, "pca033", None],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        expected_buff_array = get_buff_array()
        carte = party.decks[0].cartes["id0"]
        self.assertEqual(expected_buff_array, carte.buff["lock"])

    def test_carte_PCA033_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id1", engine.cartes["pca033"])
        player_deck.cartes["id0"].keywords = ["emperor"]
        party = unique_turn_play(
            player_play=[None, "pca033", None],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        expected_buff_array = get_buff_array(3, 1)
        expected_buff_array = get_buff_array(2, 1, expected_buff_array)
        carte = party.decks[0].cartes["id0"]
        self.assertEqual(expected_buff_array, carte.buff["lock"])

    def test_carte_PFF026_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id1", engine.cartes["pff026"])
        party = unique_turn_play(
            player_play=[None, "pff026", None],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        expected_buff_array = get_buff_array()
        result = party.resource_per_turn["energy"][0]
        self.assertEqual(expected_buff_array, result)

    def test_carte_PGB013_false(self, engine: Engine) -> None:
        player_deck = collection_deck("fearsome flyers")
        player_deck.replace_carte("id0", engine.cartes["pgb013"])
        party = unique_turn_play(
            player_play=["id1", "pgb013", "id2"],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        expected_buff_array = get_buff_array()
        for id in range(1, 18):
            result = party.decks[0].cartes[f"id{id}"].buff["power"]
            self.assertEqual(expected_buff_array, result)

    def test_carte_PHE049_true(self, engine: Engine) -> None:
        player_deck = collection_deck("herbivores")
        player_deck.replace_carte("id0", engine.cartes["phe049"])
        party = unique_turn_play(
            player_play=["id1", "phe049", "id2"],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        expected_score = array([37 + 3 * 30, 0])
        result_score = party.score[0, 0]
        self.assertEqual(expected_score, result_score)
        expected_buff_array = get_buff_array()
        for id in range(1, 3):
            result = party.decks[0].cartes[f"id{id}"].buff["power"]
            self.assertEqual(expected_buff_array, result)
        expected_buff_array = get_buff_array(1, 30)
        for id in range(3, 5):
            result = party.decks[0].cartes[f"id{id}"].buff["power"]
            self.assertEqual(expected_buff_array, result)
        expected_buff_array = get_buff_array()
        for id in range(5, 17):
            result = party.decks[0].cartes[f"id{id}"].buff["power"]
            self.assertEqual(expected_buff_array, result)

    def test_carte_PHU003_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["phu003"])
        opponent_deck = album_deck("paleontology")
        party = unique_turn_play(
            player_play=[None, "phu003", None],
            opponent_play=["id0", None, "id1"],
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        expected_score = 28
        result_score = party.score[0, 0, 0]
        self.assertEqual(expected_score, result_score)

    def test_carte_PHU003_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["phu003"])
        opponent_deck = album_deck("paleontology")
        party = unique_turn_play(
            player_play=[None, "phu003", None],
            opponent_play=[None, "id0", None],
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        expected_score = 28 + 45
        result_score = party.score[0, 0, 0]
        self.assertEqual(expected_score, result_score)

    def test_carte_PHU012_false(self, engine: Engine) -> None:
        player_deck = collection_deck("human evolution")
        player_deck.replace_carte("id0", engine.cartes["phu012"])
        opponent_deck = album_deck("paleontology")
        party = unique_turn_play(
            player_play=[None, "phu012", "id1"],
            opponent_play=[None] * 3,
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        expected_buff_array = get_buff_array()
        carte = party.decks[0].cartes["id1"]
        self.assertEqual(expected_buff_array, carte.buff["power"])
        self.assertEqual(54, party.score[0, 0, 0])

    def test_carte_PHU012_true(self, engine: Engine) -> None:
        player_deck = collection_deck("human evolution")
        player_deck.replace_carte("id0", engine.cartes["phu012"])
        player_deck.cartes["id10"].keywords = ["beetle"]
        opponent_deck = album_deck("paleontology")
        party = unique_turn_play(
            player_play=[None, "phu012", "id1"],
            opponent_play=[None] * 3,
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        expected_buff_array = get_buff_array(2, 30)
        carte = party.decks[0].cartes["id1"]
        self.assertEqual(expected_buff_array, carte.buff["power"])
        self.assertEqual(54 + 30 * 2, party.score[0, 0, 0])

    def test_carte_PMO026_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["pmo026"])
        party = unique_turn_play(
            player_play=[None, "pmo026", None],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        expected_buff_array = get_buff_array()
        for id in range(1, 18):
            carte = party.decks[0].cartes[f"id{id}"]
            self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PMO026_true(self, engine: Engine) -> None:
        player_deck = album_deck("paleontology")
        player_deck.replace_carte("id0", engine.cartes["pmo026"])
        for id in range(2, 8):
            player_deck.cartes[f"id{id}"].album = "life on land"
        party = unique_turn_play(
            player_play=["id2", "pmo026", "id1"],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        expected_score = 52 + 15
        result_score = party.score[0, 0, 0]
        self.assertEqual(expected_score, result_score)
        expected_buff_array = get_buff_array(6, 15)
        for id in range(2, 8):
            carte = party.decks[0].cartes[f"id{id}"]
            self.assertEqual(expected_buff_array, carte.buff["power"])
        expected_buff_array = get_buff_array()
        for id in range(8, 18):
            carte = party.decks[0].cartes[f"id{id}"]
            self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PLB012_1(self, engine: Engine) -> None:
        player_deck = album_deck("paleontology")
        player_deck.replace_carte("id5", engine.cartes["plb012"])
        for id in range(1, 5):
            player_deck.cartes[f"id{id}"].album = "life on land"
        party = unique_turn_play(
            player_play=["id0", "id1", "id2"],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        # Score
        expected_score = 0
        result_score = party.score[0, 0, 0]
        self.assertEqual(expected_score, result_score)
        # Hors buff
        expected_buff_array = get_buff_array()
        for id in range(0, 5):
            carte = party.decks[0].cartes[f"id{id}"]
            self.assertEqual(expected_buff_array, carte.buff["power"])
        # Buff
        expected_buff_array = get_buff_array(0, 10)
        for id in range(6, 18):
            carte = party.decks[0].cartes[f"id{id}"]
            self.assertEqual(expected_buff_array, carte.buff["power"])
        # Self
        carte = party.decks[0].cartes["plb012"]
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PLB012_2(self, engine: Engine) -> None:
        player_deck = album_deck("paleontology")
        player_deck.replace_carte("id0", engine.cartes["plb012"])
        for id in range(1, 4):
            player_deck.cartes[f"id{id}"].album = "life on land"
        party = unique_turn_play(
            player_play=["plb012", "id1", "id4"],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        # Score
        expected_score = 25 + 10 * 4
        result_score = party.score[0, 0, 0]
        self.assertEqual(expected_score, result_score)
        # Hors buff
        expected_buff_array = get_buff_array()
        for id in range(1, 4):
            carte = party.decks[0].cartes[f"id{id}"]
            self.assertEqual(expected_buff_array, carte.buff["power"])
        # Buff 1
        expected_buff_array = get_buff_array(0, 10)
        expected_buff_array = get_buff_array(1, 10, expected_buff_array)
        for id in range(5, 18):
            carte = party.decks[0].cartes[f"id{id}"]
            self.assertEqual(expected_buff_array, carte.buff["power"])
        # Buff 2
        expected_buff_array = get_buff_array(0, 10)
        carte = party.decks[0].cartes["id4"]
        self.assertEqual(expected_buff_array, carte.buff["power"])
        # Self
        expected_buff_array = get_buff_array(0, 10)
        carte = party.decks[0].cartes["plb012"]
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PCA035(self, engine: Engine) -> None:
        seed("La Vache")    # ça ne sert à rien
        player_deck = album_deck("paleontology")
        player_deck.replace_carte("id0", engine.cartes["pca035"])
        opponent_deck = dummy_deck()
        set_deck_power(opponent_deck, 100)
        party = unique_turn_play(
            player_play=["pca035", None, None],
            opponent_play=["id1", None, None],
            player_deck=player_deck,
            opponent_deck=opponent_deck,
        )
        # Score
        result_score = party.score[0, 0, 1]
        self.assertIn(result_score, [100 - 15, 100 - 15 - 20])
