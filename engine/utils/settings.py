"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .errors import *

# Python
import json

"""___Classes___________________________________________________________________________________"""


class Settings():

    _config = None

    # Settings
    project_title: str
    project_version: str
    paths: dict
    test: bool

    # CUE_Simulation
    deck_len: int
    play_len: int
    turns: int
    rounds: int

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
