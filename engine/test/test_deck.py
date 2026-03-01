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
        card = dummy_card()
        deck = Deck("test")
        cards = [card for _ in range(deck.deck_len + 1)]
        with pytest.raises(NombreIncorrectDeCartes):
            deck.create_deck(cards)

    def test_deck_keys(self) -> None:
        deck = dummy_deck()
        keys = list(deck.keys())
        self.assertEqual(len(keys), 18)
        self.assertEqual(keys[0], "id0")
        self.assertEqual(keys[-1], "id17")

    def test_replace_card(self) -> None:
        deck = dummy_deck()
        card = dummy_card()
        deck.replace_card("id0", card)
        self.assertEqual(deck.cards["dummy_card"], card)
        self.assertEqual(deck.order[0], "dummy_card")
        self.assertNotIn("id0", deck.cards)

    def test_replace_card_error(self) -> None:
        deck = dummy_deck()
        card = dummy_card()
        with pytest.raises(CarteInexistante):
            deck.replace_card("id18", card)

    def test_shuffle(self) -> None:
        expected = ["id11", "id13", "id17", "id0", "id1", "id4", "id10", "id8",
                    "id3", "id9", "id6", "id5", "id15", "id2", "id7", "id14", "id12", "id16"]
        deck = dummy_deck()
        seed("Porco Rosso")
        deck.shuffle()
        result = deck.order
        self.assertEqual(expected, result)

    def test_hand(self) -> None:
        deck = dummy_deck()
        expected = ["id0", "id1", "id2", "id3", "id4"]
        result = deck.hand
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
