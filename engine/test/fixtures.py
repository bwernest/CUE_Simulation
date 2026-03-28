"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..engine.card import Card
from ..engine.deck import Deck
from ..engine.engine import Engine
from ..engine.game import Game

# Python
import pytest
from typing import List, Literal, Optional

"""___Functions_________________________________________________________________________________"""


@pytest.fixture(scope="function")
def engine() -> Engine:
    engine = Engine("test")
    engine.start_engine()
    return engine


def dummy_deck() -> Deck:
    cards = [Card("test") for _ in range(18)]
    [card.create_card(f"id{k}", f"card{k}", album="test_album", collection="test_collection") for k, card in enumerate(cards)]
    deck = Deck("test")
    deck.create_deck(cards)
    return deck


def album_deck(album: Literal[
    "Paleontology",
    "Science",
]) -> Deck:
    deck = dummy_deck()
    for card in deck.cards.values():
        card.album = album.lower()
    return deck


def collection_deck(collection: Literal[
    "Ancient Creatures",
    "Carnivores",
    "Fearsome Flyers",
    "Groundbreakers",
    "Herbivores",
    "Land Before Time",
    "Monsters of The Deep",
    "Omnivores",
]) -> Deck:
    deck = dummy_deck()
    for card in deck.cards.values():
        card.album = "paleontology"
        card.collection = collection.lower()
    return deck


def dummy_card() -> Card:
    card = Card("test")
    card.create_card("dummy_card", "test_card")
    return card


@pytest.fixture(scope="function")
def game() -> Game:
    game = Game("test")
    game.create_game(elephant_deck(), mouse_deck(), 100, 0, 100, 100)
    return game


def elephant_deck() -> Deck:
    cards = [Card("test") for _ in range(18)]
    [card.create_card(f"id{k}", f"card{k}", power=260, cost=26) for k, card in enumerate(cards)]
    deck = Deck("test")
    deck.create_deck(cards)
    return deck


def mouse_deck() -> Deck:
    cards = [Card("test") for _ in range(18)]
    [card.create_card(f"id{k}", f"card{k}", power=10, cost=1) for k, card in enumerate(cards)]
    deck = Deck("test")
    deck.create_deck(cards)
    return deck


def unique_card_play(
    card_id: str,
    player_deck: Optional[Deck] = None,
    opponent_deck: Optional[Deck] = None,
) -> Game:
    engine = Engine("test")
    engine.start_engine()
    player_deck = dummy_deck() if player_deck is None else player_deck
    opponent_deck = dummy_deck() if opponent_deck is None else opponent_deck
    deck1 = player_deck
    deck2 = opponent_deck
    card_id = card_id.lower()
    deck1.replace_card("id0", engine.cards[card_id])
    engine.start_game(deck1, deck2, 100, 0, 0, 250, shuffle=False)
    engine.play([card_id, None, None], [None, None, None])
    return engine.game


def unique_turn_play(
    player_play: List[str | None],
    opponent_play: List[str | None],
    player_deck: Optional[Deck] = None,
    opponent_deck: Optional[Deck] = None,
) -> Game:
    engine = Engine("test")
    engine.start_engine()
    deck1 = dummy_deck() if player_deck is None else player_deck
    deck2 = dummy_deck() if opponent_deck is None else opponent_deck
    engine.start_game(deck1, deck2, 100, 0, 0, 250, shuffle=False)
    for card in player_play:
        if card is not None:
            assert card in deck1.order, "Erreur dans la rédaction du test unique_turn_play."
    for card in opponent_play:
        if card is not None:
            assert card in deck2.order, "Erreur dans la rédaction du test unique_turn_play."
    engine.play(player_play, opponent_play)
    return engine.game
