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
        for raw_card in raw_cards:
            print(raw_card)
            print()
        # for raw_card in raw_cards:
        #     card = Card(raw_card)
        #     self.cards[card.id] = card

    def get_raw_cards(self) -> List[List[Iterable]]:
        df = read_excel(self.paths["file_data"], engine="odf", sheet_name="Data")
        raw_card = []
        raw_cards = []
        for row in df.itertuples():
            row = list(row)[1:]
            if all(isna(cell) for cell in row):
                raw_cards.append(raw_card)
                raw_card = []
            else:
                # print(f"non car row = {row} et l'autre = {[float('nan')] * len(row)}")
                raw_card.append(row)
        return raw_cards
