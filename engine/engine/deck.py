"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .carte import Carte
from ..utils import *

# Python
from random import shuffle
from typing import Dict, Iterable, List

"""___Classes___________________________________________________________________________________"""


class Deck(Carte):

    cartes: Dict[str, Carte]
    order: List[str]
    remaining: List[str]

    def create_deck(self, cartes: List[Carte]):
        if not len(cartes) == self.deck_len:
            raise NombreIncorrectDeCartes("Création d'un deck")
        self.cartes = {carte.id: carte for carte in cartes}
        self.order = [carte.id for carte in cartes]
        self.remaining = []

    def copy_deck(self) -> Deck:
        new_deck = Deck(self.category)
        for key, value in self.__dict__.items():
            new_deck.__dict__[key] = value
        return new_deck

    def keys(self) -> Iterable[str]:
        return self.cartes.keys()

    def shuffle(self) -> None:
        shuffle(self.order)

    @property
    def main(self) -> List[str]:
        return self.order[:self.main_len]

    def cycle(self, cartes_jouees: List[str | None]) -> None:
        for carte in cartes_jouees:
            if carte is not None:
                if carte not in self.main:
                    raise CarteCycleeNonEnMain(f"Carte {carte} jouée mais non en main.")
                self.order.remove(carte)
                self.order.append(carte)

    def replace_carte(self, cid: str, new_carte: Carte) -> None:
        if cid not in self.cartes:
            print(f"Voilà mes id : {self.order}")
            raise CarteInexistante(f"Remplacement de la carte {cid} dans le deck.")
        del self.cartes[cid]
        self.cartes[new_carte.id] = new_carte
        self.order[self.order.index(cid)] = new_carte.id

    def get_stats(self, deck: Deck) -> Dict[str, Dict[str, int]]:
        stats = {"album": {}, "collection": {}}
        for carte in deck.cartes.values():
            for key in ["album", "collection"]:
                if carte.__getattribute__(key) not in stats[key]:
                    stats[key][carte.__getattribute__(key)] = 0
                stats[key][carte.__getattribute__(key)] += 1
        return stats

    def update_remaining(self, play: List[str | None]) -> None:
        self.remaining = self.main
        for cid in play:
            if cid is not None:
                self.remaining.remove(cid)

    @property
    def name_to_id(self) -> Dict[str, str]:
        return {name: cid for name, cid in zip([self.cartes[cid].name for cid in self.order], self.order)}
