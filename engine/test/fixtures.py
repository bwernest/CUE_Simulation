"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..engine.carte import Carte
from ..engine.deck import Deck
from ..engine.engine import Engine
from ..engine.game import Game
from ..engine.party import Party
from ..utils import *

# Python
from numpy import zeros
import pytest

"""___Functions_________________________________________________________________________________"""


@pytest.fixture(scope="function")
def engine() -> Engine:
    engine = Engine("test")
    engine.start_engine(recyclage=True)
    return engine


def dummy_deck() -> Deck:
    cartes = [Carte("test") for _ in range(18)]
    [carte.create_carte(f"id{k}", f"carte{k}", album="test_album", collection="test_collection", type="standard") for k, carte in enumerate(cartes)]
    deck = Deck("test")
    deck.create_deck(cartes)
    return deck


def album_deck(album: Literal[Album]) -> Deck:
    deck = dummy_deck()
    for carte in deck.cartes.values():
        carte.album = album
    return deck


def collection_deck(collection: Literal[Collection]) -> Deck:
    deck = dummy_deck()
    for carte in deck.cartes.values():
        carte.album = "paleontology"
        carte.collection = collection
    return deck


def dummy_carte() -> Carte:
    carte = Carte("test")
    carte.create_carte("dummy_carte", "test_carte")
    return carte


@pytest.fixture(scope="function")
def game() -> Game:
    game = Game("test")
    return game


@pytest.fixture(scope="function")
def party() -> Party:
    game = Game("test")
    party = game.create_game(elephant_deck(), mouse_deck(), 100, 0, 100, 100)
    return party


def elephant_deck() -> Deck:
    cartes = [Carte("test") for _ in range(18)]
    [carte.create_carte(f"id{k}", f"carte{k}", power=260, cost=26) for k, carte in enumerate(cartes)]
    deck = Deck("test")
    deck.create_deck(cartes)
    return deck


def mouse_deck() -> Deck:
    cartes = [Carte("test") for _ in range(18)]
    [carte.create_carte(f"id{k}", f"carte{k}", power=10, cost=1) for k, carte in enumerate(cartes)]
    deck = Deck("test")
    deck.create_deck(cartes)
    return deck


def unique_carte_play(
    cid: CarteID,
    player_deck: Optional[Deck] = None,
    opponent_deck: Optional[Deck] = None,
) -> Party:
    """
    unique_carte_play
    -----------------
    Simulation d'une partie où une unique carte est jouée par player.
    La partie est créée avec des decks par défaut ou ceux renseignés.
    La 1ère carte du player_deck (id0) est remplacée par cid.

    Paramètres
    ----------
    cid : str
        Identifiant de la carte à ajouter en 1ère position dans le player_deck.
    player_deck : Optional[Deck]
        Deck de player par défaut un dummy deck.
    opponent_deck : Optional[Deck]
        Deck de opponent par défaut un dummy deck.
    """
    engine = Engine("test")
    engine.start_engine(recyclage=True)
    player_deck = dummy_deck() if player_deck is None else player_deck
    opponent_deck = dummy_deck() if opponent_deck is None else opponent_deck
    deck1 = player_deck
    deck2 = opponent_deck
    cid = cid.lower()
    deck1.replace_carte("id0", engine.cartes[cid])
    party = engine.create_game(deck1, deck2, 100, 0, 0, 250)
    engine.start_game(party, shuffle=False)
    party = engine.play(party, [cid, None, None], [None, None, None])
    return party


def unique_turn_play(
    player_play: List[str | None],
    opponent_play: List[str | None],
    player_deck: Optional[Deck] = None,
    opponent_deck: Optional[Deck] = None,
) -> Party:
    engine = Engine("test")
    engine.start_engine(recyclage=True)
    deck1 = dummy_deck() if player_deck is None else player_deck
    deck2 = dummy_deck() if opponent_deck is None else opponent_deck
    party = engine.create_game(deck1, deck2, 100, 0, 0, 250)
    engine.start_game(party, shuffle=False)
    for carte in player_play:
        if carte is not None:
            assert carte in deck1.main, "Erreur dans la rédaction du test unique_turn_play."
    for carte in opponent_play:
        if carte is not None:
            assert carte in deck2.main, "Erreur dans la rédaction du test unique_turn_play."
    party = engine.play(party, player_play, opponent_play)
    return party


def multiple_turns_play(
    player_plays: List[List[str | None]],
    opponent_plays: List[List[str | None]],
    player_deck: Optional[Deck] = None,
    opponent_deck: Optional[Deck] = None,
) -> Party:
    engine = Engine("test")
    engine.start_engine(recyclage=True)
    deck1 = dummy_deck() if player_deck is None else player_deck
    deck2 = dummy_deck() if opponent_deck is None else opponent_deck
    party = engine.create_game(deck1, deck2, 100, 0, 0, 250)
    engine.start_game(party, shuffle=False)
    for player_play, opponent_play in zip(player_plays, opponent_plays):
        for carte in player_play:
            if carte is not None:
                assert carte in deck1.main, f"Erreur dans la rédaction du test multiple_turns_play, {carte} n'est pas en main."
        for carte in opponent_play:
            if carte is not None:
                assert carte in deck2.main, f"Erreur dans la rédaction du test multiple_turns_play, {carte} n'est pas en main."
        party = engine.play(party, player_play, opponent_play)
    return party


def set_deck_power(deck: Deck, power: int) -> None:
    for carte in deck.cartes.values():
        carte.base_power = power


def set_deck_cost(deck: Deck, cost: int) -> None:
    for carte in deck.cartes.values():
        carte.base_cost = cost


def get_buff_array(index: int = 0, value: int = 0, buff_array: Optional[NDArray] = None) -> BuffArray:
    engine = Engine("test")
    buff_array = zeros((engine.buff_array_len), dtype=int) if buff_array is None else buff_array
    buff_array[index] += value
    return buff_array
