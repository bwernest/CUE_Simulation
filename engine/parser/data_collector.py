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
            if card.id in self.cards:
                raise ValueError(f"Duplicate card id found: {card.id}")
            self.cards[card.id] = card

    def get_raw_cards(self) -> List[List[str]]:
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

    def rewrite_raw_data(self) -> None:
        raw_cards = self.get_raw_cards()
        sorted_raw_cards = self.sort_raw_cards(raw_cards)
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
                albums[card.album] = 0
            albums[card.album] += 1
        print("\nAlbums :")
        for album, count in albums.items():
            print(f"{album}: {count}")

    def print_collection(self, collection: str) -> None:
        print(f"\nCollection {collection} :")
        sorted_cards = sorted(self.cards.values(), key=lambda c: c.name)
        for card in sorted_cards:
            if card.collection == collection:
                print(f"{card.id} - {card.name}")

    def print_cards_collections(self) -> None:
        collections = {}
        for card in self.cards.values():
            if card.collection not in collections:
                collections[card.collection] = 0
            collections[card.collection] += 1
        print("\nCollections :")
        for collection in sorted(collections.keys()):
            print(f"{collection}: {collections[collection]}")

    def sort_raw_cards(self, raw_cards: List[List[str]]) -> List[List[str]]:
        lenC = len(raw_cards)
        for i in range(lenC - 1):
            for j in range(lenC - 1):
                if not self.check_alphabetical_order(raw_cards[j][0][0][:3], raw_cards[j + 1][0][0][:3]):
                    temp = raw_cards[j + 1]
                    raw_cards[j + 1] = raw_cards[j]
                    raw_cards[j] = temp
                elif raw_cards[j][0][0][:3] == raw_cards[j + 1][0][0][:3]:
                    if not self.check_alphabetical_order(raw_cards[j][0][1], raw_cards[j + 1][0][1]):
                        temp = raw_cards[j + 1]
                        raw_cards[j + 1] = raw_cards[j]
                        raw_cards[j] = temp
        return raw_cards

    def check_alphabetical_order(self, string1: str, string2: str) -> bool:
        """Check if string1 is alphabetically before string2."""
        len1 = len(string1)
        len2 = len(string2)
        index = 0
        while index < len1 and index < len2:
            if string1[index] < string2[index]:
                return True
            elif string1[index] > string2[index]:
                return False
            index += 1
        return len1 <= len2

    def get_check_raw_cards(self) -> Dict[str, List[str]]:
        raw_cards = self.get_raw_cards()
        row_filled, column_filled = True, True
        row, column = 0, 0
        data = {}
        while row_filled:
            row_filled = False
            while column < 10:
                column_filled = False
                data[f"{row}.{column}"] = []
                for raw_card in raw_cards:
                    try:
                        data[f"{row}.{column}"].append(raw_card[row][column])
                        row_filled = True
                        column_filled = True
                    except IndexError: pass
                column += 1
            row += 1
            column = 0
        return data

    def print_check_raw_cards(self) -> None:
        data = self.get_check_raw_cards()
        for key, value in data.items():
            if value == [] or isna(value[0]): continue
            cvalue = {val:value.count(val) for val in value}
            print("\n")
            print(f"{key} : {cvalue}")
