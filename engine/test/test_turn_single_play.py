"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

"""___Tests_____________________________________________________________________________________"""


class TestTurnSinglePlay(Assert):

    def test_carte_PMO030_true(self, engine: Engine) -> None:
        player_deck = collection_deck("Monsters of The Deep")
        player_deck.replace_carte("id0", engine.cartes["pmo030"])
        game = unique_turn_play(["id1", "pmo030", "id2"], [None] * 3, player_deck)
        carte = game.decks[0].cartes["pmo030"]
        self.assertEqual(carte.base_power + 15 * 3, game.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PMO030_false(self, engine: Engine) -> None:
        player_deck = album_deck("Paleontology")
        player_deck.replace_carte("id0", engine.cartes["pmo030"])
        game = unique_turn_play(["id1", "pmo030", None], [None] * 3, player_deck)
        carte = game.decks[0].cartes["pmo030"]
        self.assertEqual(carte.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PCA045_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["pca045"])
        player_deck.replace_carte("id1", engine.cartes["pca013"])
        game = unique_turn_play(["pca013", "pca045", None], [None] * 3, player_deck)

        carte_45 = game.decks[0].cartes["pca045"]
        carte_13 = game.decks[0].cartes["pca013"]
        self.assertEqual(carte_45.base_power + carte_13.base_power + 15 * 2 + 6, game.score[0, 0, 0])
        self.assertEqual(100 - carte_45.base_cost - carte_13.base_cost, game.energy[0])

        expected_buff_array = get_buff_array(3, 15)
        self.assertEqual(expected_buff_array, carte_45.buff["power"])
        self.assertEqual(expected_buff_array, carte_13.buff["power"])

        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, game.resource_per_turn["power"][0])

    def test_carte_PCA045_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["pca045"])
        player_deck.replace_carte("id1", engine.cartes["pca013"])
        game = unique_turn_play(["pca013", None, "pca045"], [None] * 3, player_deck)

        carte_45 = game.decks[0].cartes["pca045"]
        carte_13 = game.decks[0].cartes["pca013"]
        self.assertEqual(carte_45.base_power + carte_13.base_power + 6, game.score[0, 0, 0])
        self.assertEqual(100 - carte_45.base_cost - carte_13.base_cost, game.energy[0])

        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte_45.buff["power"])
        self.assertEqual(expected_buff_array, carte_13.buff["power"])
        self.assertEqual(expected_buff_array, game.resource_per_turn["power"][0])

    def test_carte_PMO040_false(self, engine: Engine) -> None:
        player_deck = album_deck("Paleontology")
        player_deck.replace_carte("id0", engine.cartes["pmo040"])
        game = unique_turn_play(["pmo040", "id1", "id2"], [None] * 3, player_deck)
        carte = game.decks[0].cartes["pmo040"]
        self.assertEqual(carte.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, game.energy[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PMO040_true(self, engine: Engine) -> None:
        player_deck = album_deck("Science")
        player_deck.replace_carte("id0", engine.cartes["pmo040"])
        game = unique_turn_play(["pmo040", "id1", "id2"], [None] * 3, player_deck)
        carte = game.decks[0].cartes["pmo040"]
        self.assertEqual(carte.base_power + 20, game.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, game.energy[0])
        expected_buff_array = get_buff_array(2, 20)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PAN058_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["pan058"])
        player_deck.replace_carte("id1", engine.cartes["sbb001"])
        game = unique_turn_play(["sbb001", "pan058", None], [None] * 3, player_deck)
        carteP = game.decks[0].cartes["pan058"]
        carteS = game.decks[0].cartes["sbb001"]
        self.assertEqual(carteP.base_power + 9 + 60 + carteS.base_power, game.score[0, 0, 0])
        self.assertEqual(100 - carteP.base_cost + 1 - carteS.base_cost, game.energy[0])
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
        game = unique_turn_play(["id0", "id1", "id3"], ["id4", "id2", "id1"], player_deck, opponent_deck)
        carte = game.decks[0].cartes["pca027"]
        self.assertEqual(100 - (10 + 1) * 3 + 3, game.energy[0])
        self.assertEqual(100 - (10 + 1) * 3, game.energy[1])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["cost"])

    def test_carte_POM020(self, engine: Engine) -> None:
        player_deck = album_deck("Paleontology")
        player_deck.replace_carte("id0", engine.cartes["pom020"])
        opponent_deck = dummy_deck()
        set_deck_power(opponent_deck, 100)
        game = unique_turn_play(["pom020", None, None], ["id4", "id2", "id1"], player_deck, opponent_deck)
        carteA = game.decks[0].cartes["pom020"]
        carte1 = game.decks[0].cartes["id1"]
        self.assertEqual(carteA.base_power, game.score[0, 0, 0])
        self.assertEqual(3 * 100, game.score[0, 0, 1])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carteA.buff["power"])
        expected_buff_array = get_buff_array(3, 20)
        self.assertEqual(expected_buff_array, carte1.buff["power"])
        expected_buff_array = get_buff_array(2, 35)
        self.assertEqual(expected_buff_array, game.resource_per_turn["power"][0])

    def test_carte_PHE024_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id0", engine.cartes["phe014"])
        player_deck.replace_carte("id1", engine.cartes["phe024"])
        game = unique_turn_play(
            player_play=[None, "phe024", None],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        carte = game.decks[0].cartes["phe014"]
        expected_buff_array = get_buff_array(0, 49)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PHE024_false(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id5", engine.cartes["phe014"])
        player_deck.replace_carte("id1", engine.cartes["phe024"])
        game = unique_turn_play(
            player_play=[None, "phe024", None],
            opponent_play=[None] * 3,
            player_deck=player_deck,
        )
        carte = game.decks[0].cartes["phe014"]
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])
