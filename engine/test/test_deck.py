"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.deck import Deck

# Python
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
