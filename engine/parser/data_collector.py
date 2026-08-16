"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..engine.carte import Carte
from ..engine.game import Game
from ..utils import *

# Python
from pandas import read_excel, DataFrame, isna
from typing import Dict, Iterable, List

"""___Classes___________________________________________________________________________________"""


class DataCollector(Game):

    cartes: Dict[str, Carte]

    def collect_data(self, recyclage: bool = True) -> None:
        if recyclage and self.recycler_cartes():
            return
        raw_cartes = self.get_raw_cartes()
        self.cartes = {}
        for raw_carte in raw_cartes:
            carte = Carte()
            carte.create_carte_from_data(raw_carte)
            if carte.id in self.cartes:
                raise ValueError(f"Carte en double : {carte.id}")
            self.cartes[carte.id] = carte
        self.pickle_save(self.paths["file_cartes_pickle"], self.cartes)
        self.pickle_save(self.paths["file_cartes_pickle_size"], os.path.getsize(self.paths["file_data"]))

    def recycler_cartes(self) -> bool:
        """
        recycler_cartes
        ---------------
        Fonction qui tente de récupérer les cartes précédemment créées. Le but est
        d'éviter de recréer toutes les cartes à chaque fois. Ainsi la taille du fichier
        source est comparée à la taille précédemment enregistrée.
        """
        cartes_pickle = self.pickle_load(self.paths["file_cartes_pickle"])
        if cartes_pickle is None:
            self.add_log("Pas de pickle trouvé !")
            return False
        old_size = self.pickle_load(self.paths["file_cartes_pickle_size"])
        current_size = os.path.getsize(self.paths["file_data"])
        if old_size == current_size:
            self.cartes = cartes_pickle
            self.add_log("Vielles cartes récupérées !")
            return True
        else:
            self.add_log("Nouvelles cartes différentes !")
            return False

    def get_raw_cartes(self) -> List[List[str]]:
        df = read_excel(self.paths["file_data"], engine="odf", sheet_name="Data")
        raw_carte = []
        raw_cartes = []
        for row in df.itertuples():
            row = list(row)[1:]
            if all(isna(cell) for cell in row):
                raw_cartes.append(raw_carte)
                if len(raw_carte) == 0:
                    raise ValueError("Empty raw carte found")
                raw_carte = []
            else:
                raw_carte.append(row)
        raw_cartes.append(raw_carte)
        return raw_cartes

    def rewrite_raw_data(self) -> None:
        raw_cartes = self.get_raw_cartes()
        sorted_raw_cartes = self.sort_raw_cartes(raw_cartes)
        txt = "A\n"
        for raw_carte in sorted_raw_cartes:
            for line in raw_carte:
                for data in line:
                    if isna(data):
                        data = ""
                    txt += str(data) + "\t"
                txt += "\n"
            txt += "\n"
        self.write_txt(f"{self.paths["folder_data"]}/new_cartes.txt", txt)

    def print_cartes_albums(self) -> None:
        albums = {}
        for carte in self.cartes.values():
            if carte.album not in albums:
                albums[carte.album] = 0
            albums[carte.album] += 1
        print("\nAlbums :")
        for album, count in albums.items():
            print(f"{album}: {count}")

    def print_collection(self, collection: str) -> None:
        print(f"\nCollection {collection} :")
        sorted_cartes = sorted(self.cartes.values(), key=lambda c: c.name)
        for carte in sorted_cartes:
            if carte.collection == collection:
                print(f"{carte.id} - {carte.name}")

    def print_cartes_collections(self) -> None:
        collections = {}
        for carte in self.cartes.values():
            if carte.collection not in collections:
                collections[carte.collection] = 0
            collections[carte.collection] += 1
        print("\nCollections :")
        for collection in sorted(collections.keys()):
            print(f"{collection}: {collections[collection]}")

    def sort_raw_cartes(self, raw_cartes: List[List[str]]) -> List[List[str]]:
        lenC = len(raw_cartes)
        for i in range(lenC - 1):
            for j in range(lenC - 1):
                if not self.check_alphabetical_order(raw_cartes[j][0][0][:3], raw_cartes[j + 1][0][0][:3]):
                    temp = raw_cartes[j + 1]
                    raw_cartes[j + 1] = raw_cartes[j]
                    raw_cartes[j] = temp
                elif raw_cartes[j][0][0][:3] == raw_cartes[j + 1][0][0][:3]:
                    if not self.check_alphabetical_order(raw_cartes[j][0][1], raw_cartes[j + 1][0][1]):
                        temp = raw_cartes[j + 1]
                        raw_cartes[j + 1] = raw_cartes[j]
                        raw_cartes[j] = temp
        return raw_cartes

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

    def get_check_raw_cartes(self) -> Dict[str, List[str]]:
        raw_cartes = self.get_raw_cartes()
        row_filled, column_filled = True, True
        row, column = 0, 0
        data = {}
        while row_filled:
            row_filled = False
            while column < 10:
                column_filled = False
                data[f"{row}.{column}"] = []
                for raw_carte in raw_cartes:
                    try:
                        data[f"{row}.{column}"].append(raw_carte[row][column])
                        row_filled = True
                        column_filled = True
                    except IndexError:
                        pass
                column += 1
            row += 1
            column = 0
        return data

    def print_check_raw_cartes(self) -> None:
        data = self.get_check_raw_cartes()
        for key, value in data.items():
            if value == [] or isna(value[0]):
                continue
            cvalue = {val: value.count(val) for val in value}
            print("\n")
            print(f"{key} : {cvalue}")
