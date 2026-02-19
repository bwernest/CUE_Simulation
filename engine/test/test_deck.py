"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.deck import Deck

# Python
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestDeck(Assert):

    def test_create_deck_error1(self, dummy_card: Card) -> None:
        deck = Deck("test")
        cards = [dummy_card for _ in range(17)]
        with pytest.raises(NombreIncorrectDeCartes):
            deck.create_deck(cards)

    def test_deck_keys(self, dummy_deck: Deck) -> None:
        keys = list(dummy_deck.keys())
        print(keys)
        self.assertEqual(len(keys), 18)
        self.assertEqual(keys[0], "id0")
        self.assertEqual(keys[-1], "id17")
