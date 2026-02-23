"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .card import Card
from ..utils import *

# Python
from random import shuffle
from typing import Dict, Iterable, List

"""___Classes___________________________________________________________________________________"""


class Deck(Card):

    cards: Dict[str, Card]
    order: List[str]

    def create_deck(self, cards: List[Card]):
        if not len(cards) == self.deck_len:
            raise NombreIncorrectDeCartes("Création d'un deck")
        self.cards = {card.id: card for card in cards}
        self.order = [card.id for card in cards]

    def keys(self) -> Iterable[str]:
        return self.cards.keys()

    def shuffle(self) -> None:
        shuffle(self.order)

    @property
    def hand(self) -> List[str]:
        return self.order[:self.hand_len]

    def cycle(self, cards_played: List[str | None]) -> None:
        for card in cards_played:
            if card is not None:
                self.order.remove(card)
                self.order.append(card)
