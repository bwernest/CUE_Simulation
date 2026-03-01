"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..engine.card import Card
from ..engine.game import Game
from ..utils import *

# Python
from pandas import read_excel, DataFrame, isna
from typing import Dict, Iterable, List

"""___Classes___________________________________________________________________________________"""


class DataCollector(Game):

    cards: Dict[str, Card]

    def collect_data(self) -> None:
        raw_cards = self.get_raw_cards()
        self.cards = {}
        for raw_card in raw_cards:
            card = Card()
            card.create_card_from_data(raw_card)
            self.cards[card.id] = card

    def get_raw_cards(self) -> List[List[Iterable]]:
        df = read_excel(self.paths["file_data"], engine="odf", sheet_name="Data")
        raw_card = []
        raw_cards = []
        for row in df.itertuples():
            row = list(row)[1:]
            if all(isna(cell) for cell in row):
                raw_cards.append(raw_card)
                if len(raw_card) == 0:
                    raise ValueError("Empty raw card found")
                raw_card = []
            else:
                raw_card.append(row)
        raw_cards.append(raw_card)
        return raw_cards

    def write_raw_data(self) -> None:
        raw_cards = self.get_raw_cards()
        sorted_raw_cards = sorted(raw_cards, key=lambda x: x[0][0])
        txt = "A\n"
        for raw_card in sorted_raw_cards:
            for line in raw_card:
                for data in line:
                    if isna(data):
                        data = ""
                    txt += str(data) + "\t"
                txt += "\n"
            txt += "\n"
        self.write_txt(f"{self.paths["folder_data"]}/new_cartes.txt", txt)

    def print_cards_albums(self) -> None:
        albums = {}
        for card in self.cards.values():
            if card.album not in albums:
                albums[card.album] = 1
            albums[card.album] += 1
        print("\nAlbums :")
        for album, count in albums.items():
            print(f"{album}: {count}")

    def print_cards_collections(self) -> None:
        collections = {}
        for card in self.cards.values():
            if card.collection not in collections:
                collections[card.collection] = 1
            collections[card.collection] += 1
        print("\nCollections :")
        for collection, count in collections.items():
            print(f"{collection}: {count}")
