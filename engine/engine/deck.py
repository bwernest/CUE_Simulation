"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .card import Card
from ..utils import *

# Python
from typing import Dict, Iterable, List

"""___Classes___________________________________________________________________________________"""


class Deck(Card):

    cards: Dict[str, Card]

    def create_deck(self, cards: List[Card]):
        if not len(cards) == self.deck_len: raise NombreIncorrectDeCartes("Création d'un deck")
        self.cards = {card.id: card for card in cards}

    def keys(self) -> Iterable[str]:
        return self.cards.keys()
