"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..engine.card import Card
from ..engine.deck import Deck
from ..engine.engine import Engine
from ..engine.game import Game

# Python
from copy import deepcopy
import pytest

"""___Functions_________________________________________________________________________________"""


@pytest.fixture(scope="class")
def engine() -> Engine:
    engine = Engine("test")
    return engine

@pytest.fixture(scope="class")
def dummy_deck() -> list:
    cards = [Card("test") for k in range(18)]
    [card.create_card(f"id{k}", f"card{k}") for k, card in enumerate(cards)]
    deck = Deck("test")
    deck.create_deck(cards)
    return deck

@pytest.fixture(scope="class")
def dummy_card() -> Card:
    card = Card("test")
    card.create_card("dummy_card", "test_card")
    return card

@pytest.fixture(scope="class")
def game() -> Game:
    game = Game("test")
    game.create_game(elephant_deck(), mouse_deck())
    return game

def elephant_deck() -> Deck:
    cards = [Card("test") for _ in range(18)]
    [card.create_card(f"id{k}", f"card{k}", power=260, energy=26) for k, card in enumerate(cards)]
    deck = Deck("test")
    deck.create_deck(cards)
    return deck

def mouse_deck() -> Deck:
    cards = [Card("test") for _ in range(18)]
    [card.create_card(f"id{k}", f"card{k}", power=10, energy=1) for k, card in enumerate(cards)]
    deck = Deck("test")
    deck.create_deck(cards)
    return deck