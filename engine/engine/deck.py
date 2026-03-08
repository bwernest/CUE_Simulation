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
    remaining: List[str]

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
                if card not in self.hand:
                    raise CarteCycleeNonEnMain(f"Carte {card} jouée mais non en main.")
                self.order.remove(card)
                self.order.append(card)

    def replace_card(self, card_id: str, new_card: Card) -> None:
        if card_id not in self.cards:
            raise CarteInexistante(f"Remplacement de la carte {card_id} dans le deck.")
        del self.cards[card_id]
        self.cards[new_card.id] = new_card
        self.order[self.order.index(card_id)] = new_card.id

    def get_stats(self, deck: Deck) -> Dict[str, int]:
        stats = {"album": {}, "collection": {}}
        for card in deck.cards.values():
            for key in ["album", "collection"]:
                if card.__getattribute__(key) not in stats[key]:
                    stats[key][card.__getattribute__(key)] = 0
                stats[key][card.__getattribute__(key)] += 1
        return stats


    def update_remaining(self, play: List[str | None]) -> None:
        self.remaining = self.hand
        for card_id in play:
            if card_id is not None:
                self.remaining.remove(card_id)