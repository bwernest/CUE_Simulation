"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *

# Python
from numpy import array, sum

"""___Tests_____________________________________________________________________________________"""


class TestCarteSinglePlay(Assert):

    def test_carte_MYPA001(self) -> None:
        party = unique_carte_play("MYPA001")
        carte = party.decks[0].cartes["mypa001"]
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, party.resource_per_turn["energy"][0])
        self.assertEqual(carte.base_power + 77, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        self.assertEqual({
            "album": {"paleontology": 1, "test_album": 17},
            "collection": {"paleontology mythic cards": 1, "test_collection": 17}
        }, party.stats[0])

    def test_carte_PCA002(self) -> None:
        party = unique_carte_play("PCA002")
        carte = party.decks[0].cartes["pca002"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])

    def test_carte_PAN015(self) -> None:
        party = unique_carte_play("PAN015")
        carte = party.decks[0].cartes["pan015"]
        self.assertEqual(carte.base_power + 24, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        self.assertEqual(get_buff_array(), carte.buff["power"])
        self.assertEqual(get_buff_array(2, -1), carte.buff["cost"])

    def test_carte_PCA038(self) -> None:
        party = unique_carte_play("PCA038")
        carte = party.decks[0].cartes["pca038"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(array([100 - carte.base_cost + 5, 100]), party.energie)

    def test_carte_PHE017(self) -> None:
        party = unique_carte_play("PHE017")
        carte = party.decks[0].cartes["phe017"]
        self.assertEqual(carte.base_power + 8, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        self.assertEqual(get_buff_array(0, 8), carte.buff["power"])

    def test_carte_PAN024(self) -> None:
        party = unique_carte_play("PAN024")
        carte = party.decks[0].cartes["pan024"]
        total_main_buff = int(sum([sum(party.decks[0].cartes[cid].buff["power"]) for cid in party.decks[0].main]))
        self.assertIn(total_main_buff, [0, 46, 46 * 2])
        self.assertIn(party.score[0, 0, 0], [carte.base_power, carte.base_power + 46])
        self.assertEqual(100 - carte.base_cost, party.energie[0])

    def test_carte_PHE026(self) -> None:
        party = unique_carte_play("PHE026")
        carte = party.decks[0].cartes["phe026"]
        self.assertEqual(get_buff_array(0, 3), party.resource_per_turn["power"][0])
        self.assertEqual(carte.base_power + 3, party.score[0, 0, 0])
        self.assertEqual(get_buff_array(0, -1), carte.buff["cost"])
        self.assertEqual(100 - carte.base_cost + 1, party.energie[0])

    def test_carte_PAN045(self) -> None:
        party = unique_carte_play("PAN045")
        carte = party.decks[0].cartes["pan045"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])

    def test_carte_PAN046(self) -> None:
        party = unique_carte_play("PAN046")
        carte = party.decks[0].cartes["pan046"]
        self.assertEqual(carte.base_power + 20, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])
        self.assertEqual(expected_buff_array, carte.buff["cost"])

    def test_carte_PAN022_false(self) -> None:
        party = unique_carte_play("PAN022")
        carte = party.decks[0].cartes["pan022"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, party.resource_per_turn["power"][0])

    def test_carte_PAN022_true(self) -> None:
        party = unique_carte_play("PAN022", album_deck("paleontology"))
        carte = party.decks[0].cartes["pan022"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array(3, 25)
        self.assertEqual(expected_buff_array, party.resource_per_turn["power"][0])

    def test_carte_PCA023(self) -> None:
        party = unique_carte_play("PCA023", album_deck("paleontology"))
        carte = party.decks[0].cartes["pca023"]
        self.assertEqual(carte.base_power + 35, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array(3, 35)
        self.assertEqual(expected_buff_array, carte.buff["power"])
        self.assertEqual(expected_buff_array, party.decks[0].cartes["id1"].buff["power"])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, party.decks[1].cartes["id1"].buff["power"])

    def test_carte_PIC008(self) -> None:
        deck = album_deck("paleontology")
        for cid in range(10):
            deck.cartes[f"id{cid}"].base_cost = 10
        for cid in range(0, 3):
            deck.cartes[f"id{cid}"].rarity = "rare"
        for cid in range(3, 6):
            deck.cartes[f"id{cid}"].rarity = "epic"
        for cid in range(6, 9):
            deck.cartes[f"id{cid}"].rarity = "legendary"

        party = unique_carte_play("PIC008", deck)
        carte = party.decks[0].cartes["pic008"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost + 1, party.energie[0])

        for cid in range(1, 3):
            self.assertEqual(-1, deck.cartes[f"id{cid}"].buff["cost"][0])
        for cid in range(3, 6):
            self.assertEqual(-1, deck.cartes[f"id{cid}"].buff["cost"][0])
        for cid in range(6, 9):
            self.assertEqual(0, deck.cartes[f"id{cid}"].buff["cost"][0])

    def test_carte_PAN058(self) -> None:
        party = unique_carte_play("PAN058")
        carte = party.decks[0].cartes["pan058"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost + 1, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])
        expected_buff_array = get_buff_array(2, -1)
        self.assertEqual(expected_buff_array, carte.buff["cost"])

    def test_carte_PMO030(self) -> None:
        party = unique_carte_play("PMO030")
        carte = party.decks[0].cartes["pmo030"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PMO045_false(self) -> None:
        party = unique_carte_play("PMO045")
        carte = party.decks[0].cartes["pmo045"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PMO045_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        for cid, carte in player_deck.cartes.items():
            carte.album = cid    # type:ignore
        party = unique_carte_play("PMO045", player_deck)
        carte = party.decks[0].cartes["pmo045"]
        self.assertEqual(carte.base_power + 20, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array(0, 10)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PMO040(self) -> None:
        party = unique_carte_play("PMO040")
        carte = party.decks[0].cartes["pmo040"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PAN063(self) -> None:
        party = unique_carte_play("PAN063")
        carte = party.decks[0].cartes["pan063"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])

    def test_carte_PHU013(self) -> None:
        party = unique_carte_play("PHU013")
        carte = party.decks[0].cartes["phu013"]
        self.assertEqual(carte.base_power + 9, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array(0, 9)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PIC023(self) -> None:
        party = unique_carte_play("PIC023")
        carte = party.decks[0].cartes["pic023"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PCA036(self) -> None:
        player_deck = dummy_deck()
        opponent_deck = dummy_deck()
        set_deck_power(player_deck, 100)
        set_deck_power(opponent_deck, 100)
        party = unique_carte_play("PCA036", player_deck=player_deck, opponent_deck=opponent_deck)
        carte = party.decks[0].cartes["pca036"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

        expected_buff_array = get_buff_array(2, -50)
        for player in range(2):
            for cid in party.decks[player].remaining:
                self.assertEqual(expected_buff_array, party.decks[player].cartes[cid].buff["power"])

    def test_carte_PFF038(self) -> None:
        party = unique_carte_play("PFF038")
        carte = party.decks[0].cartes["pff038"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PFF023(self) -> None:
        party = unique_carte_play("PFF023")
        carte = party.decks[0].cartes["pff023"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])

    def test_carte_PHE028(self) -> None:
        party = unique_carte_play("PHE028")
        carte = party.decks[0].cartes["phe028"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, party.resource_per_turn["energy"][0])

    def test_carte_PCA003(self) -> None:
        party = unique_carte_play("PCA003")
        carte = party.decks[0].cartes["pca003"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(-12, party.score[0, 0, 1])
        expected_buff_array = get_buff_array(3, -12)
        self.assertEqual(expected_buff_array, party.resource_per_turn["power"][1])

    def test_carte_PLB006_1(self) -> None:
        player_deck = album_deck("paleontology")
        party = unique_carte_play("PLB006", player_deck=player_deck)
        carte = party.decks[0].cartes["plb006"]
        self.assertEqual(carte.base_power - 10, party.score[0, 0, 0])
        expected_buff_array = get_buff_array(0, -10)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PLB006_2(self) -> None:
        player_deck = album_deck("science")
        party = unique_carte_play("PLB006", player_deck=player_deck)
        carte = party.decks[0].cartes["plb006"]
        self.assertEqual(carte.base_power - 20, party.score[0, 0, 0])
        expected_buff_array = get_buff_array(0, -20)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PCA027(self) -> None:
        party = unique_carte_play("PCA027")
        carte = party.decks[0].cartes["pca027"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost - 1 + 3, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["cost"])

    def test_carte_POM020(self) -> None:
        party = unique_carte_play("POM020")
        carte = party.decks[0].cartes["pom020"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_PHE014(self) -> None:
        party = unique_carte_play("PHE014")
        carte = party.decks[0].cartes["phe014"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])

    def test_carte_PHE024(self) -> None:
        party = unique_carte_play("PHE024")
        carte = party.decks[0].cartes["phe024"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])

    def test_carte_PAN052_false(self) -> None:
        party = unique_carte_play("PAN052")
        carte = party.decks[0].cartes["pan052"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])

    def test_carte_PAN052_true(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id10", engine.cartes["ore018"])
        party = unique_carte_play("PAN052", player_deck)
        carte = party.decks[0].cartes["ore018"]
        expected_buff_array = get_buff_array(2, 25)
        self.assertEqual(expected_buff_array, carte.buff["power"])

    def test_carte_ORE018(self) -> None:
        opponent_deck = dummy_deck()
        set_deck_power(opponent_deck, 40)
        party = unique_carte_play("ORE018")
        carte = party.decks[0].cartes["ore018"]
        self.assertEqual(carte.base_power, party.score[0, 0, 0])
        self.assertEqual(100 - carte.base_cost, party.energie[0])
        expected_buff_array = get_buff_array()
        self.assertEqual(expected_buff_array, party.decks[1].cartes["id0"].buff["power"])

        expected_lock_statuses = [
            {"id1": 0, "id2": 0, "id3": 0, "id4": 0, "id5": 0},
            {"id0": 0, "id1": 0, "id2": 0, "id3": 0, "id4": 0},
        ]
        self.assertEqual(expected_lock_statuses, party.get_lock_statuses())

    def test_carte_PCA022(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        player_deck.replace_carte("id5", engine.cartes["pca022"])
        party = unique_carte_play("MYPA001", player_deck)
        carte = party.decks[0].cartes["pca022"]
        expected_buff_array = get_buff_array(2, 1)
        expected_buff_array = get_buff_array(3, 1, expected_buff_array)
        self.assertEqual(expected_buff_array, carte.buff["lock"])
        expected_lock_statuses = [
            {"id1": 0, "id2": 0, "id3": 0, "id4": 0, "pca022": 2},
            {"id0": 0, "id1": 0, "id2": 0, "id3": 0, "id4": 0},
        ]
        self.assertEqual(expected_lock_statuses, party.get_lock_statuses())

    def test_carte_SCD004(self, engine: Engine) -> None:
        player_deck = collection_deck("hoaxes and cons")
        opponent_deck = collection_deck("hoaxes and cons")
        opponent_deck.replace_carte("id0", engine.cartes["pca022"])
        party = unique_carte_play("scd004", player_deck, opponent_deck)

        # Carte testée
        carte = party.decks[0].cartes["scd004"]
        expected_buff_array = get_buff_array(0, 25)
        self.assertEqual(expected_buff_array, carte.buff["power"])

        # Autres cartes
        expected_buff_array = get_buff_array(0, -5)
        for deck in party.decks:
            for cid, carte in deck.cartes.items():
                if cid.startswith("id"):
                    self.assertEqual(expected_buff_array, carte.buff["power"])
                elif cid != "scd004":
                    self.assertEqual(zeros((engine.buff_array_len)), carte.buff["power"])

    def test_carte_PAN026(self, engine: Engine) -> None:
        player_deck = dummy_deck()
        party = unique_carte_play("pan026", player_deck)
        # Score
        expected_score = array([37, 0])
        result_score = party.score[0, 0]
        self.assertEqual(expected_score, result_score)
        # Buff 1
        expected_buff_array = get_buff_array(1, 10)
        for carte in party.decks[0].cartes.values():
            self.assertEqual(expected_buff_array, carte.buff["power"])
        # Buff 2
        expected_buff_array = get_buff_array(0, -5)
        for carte in party.decks[1].cartes.values():
            self.assertEqual(expected_buff_array, carte.buff["power"])
