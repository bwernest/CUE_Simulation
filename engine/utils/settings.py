"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .errors import *

# Python
import json
from typing import Dict, Literal

"""___Classes___________________________________________________________________________________"""


class Settings():

    _config = None

    # Settings
    project_title: str
    project_version: str
    paths: Dict[Literal[
        "file_data",
        "folder_data",
        "file_save",
        "file_log",
        "file_cartes_pickle",
    ], str]
    test: bool

    # CUE_Simulation
    deck_len: int
    play_len: int
    hand_len: int
    turns: int
    rounds: int
    start_energy: int
    energy_per_turn: int
    min_energy: int
    max_energy: int

    buff_array_len: int

    def __init__(self, category: str = "prod") -> None:
        if Settings._config is None:

            with open("engine/settings.json") as file:
                Settings._config = json.load(file)

        # Paramètres universels
        self.category = category
        for key, value in Settings._config.items():
            if not isinstance(value, dict):
                setattr(self, key, value)

        # Paramètres de configuration
        try:
            for key, value in Settings._config[category].items():
                setattr(self, key, value)
        except KeyError:
            raise SettingsNotAvailable(
                f"Paramètres {category} inexistants ou non répertoriés.")
