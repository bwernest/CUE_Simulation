"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.deck import Deck

# Python
from random import seed
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestDeck(Assert):

    def test_create_deck_error1(self) -> None:
        carte = dummy_carte()
        deck = Deck("test")
        cartes = [carte for _ in range(deck.deck_len + 1)]
        with pytest.raises(NombreIncorrectDeCartes):
            deck.create_deck(cartes)

    def test_deck_keys(self) -> None:
        deck = dummy_deck()
        keys = list(deck.keys())
        self.assertEqual(len(keys), 18)
        self.assertEqual(keys[0], "id0")
        self.assertEqual(keys[-1], "id17")

    def test_replace_carte(self) -> None:
        deck = dummy_deck()
        carte = dummy_carte()
        deck.replace_carte("id0", carte)
        self.assertEqual(deck.cartes["dummy_carte"], carte)
        self.assertEqual(deck.order[0], "dummy_carte")
        self.assertNotIn("id0", deck.cartes)

    def test_replace_carte_error(self) -> None:
        deck = dummy_deck()
        carte = dummy_carte()
        with pytest.raises(CarteInexistante):
            deck.replace_carte("id18", carte)

    def test_shuffle1(self) -> None:
        expected = ["id11", "id13", "id17", "id0", "id1", "id4", "id10", "id8",
                    "id3", "id9", "id6", "id5", "id15", "id2", "id7", "id14", "id12", "id16"]
        deck = dummy_deck()
        seed("Porco Rosso")
        deck.shuffle()
        result = deck.order
        self.assertEqual(expected, result)

    def test_shuffle2(self) -> None:
        expected = ["id11", "id0", "id6", "id9", "id14", "id3", "id2", "id1", "id15",
                    "id7", "id16", "id17", "id13", "id4", "id10", "id12", "id5", "id8"]
        deck = dummy_deck()
        game = Game("test")
        party = game.create_game(deck, deck, 100, 0, 0, 250)
        seed("Porco Rosso")
        game.start_game(party)
        result = party.decks[0].order
        self.assertEqual(expected, result)

    def test_main(self) -> None:
        deck = dummy_deck()
        expected = ["id0", "id1", "id2", "id3", "id4"]
        result = deck.main
        self.assertEqual(expected, result)

    def test_cycle(self) -> None:
        deck = dummy_deck()
        expected = ["id0", "id2", "id3", "id5", "id6", "id7", "id8", "id9", "id10",
                    "id11", "id12", "id13", "id14", "id15", "id16", "id17", "id1", "id4"]
        deck.cycle(["id1", "id4", None])
        result = deck.order
        self.assertEqual(expected, result)

    def test_cycle_error(self) -> None:
        deck = dummy_deck()
        with pytest.raises(CarteCycleeNonEnMain):
            deck.cycle(["id15", None, None])

    def test_name_to_id(self) -> None:
        expected = {f"carte{k}": f"id{k}" for k in range(18)}
        deck = dummy_deck()
        result = deck.name_to_id
        self.assertEqual(expected, result)
