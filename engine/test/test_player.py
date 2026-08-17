"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.engine import Engine

# Python
from copy import deepcopy

"""___Tests_____________________________________________________________________________________"""


class TestPlayer(Assert):

    class TestPlayer_GetPlay(Assert):

        def test_get_play_1(self, engine: Engine) -> None:
            party = engine.create_game(dummy_deck(), dummy_deck(), 100, 0, 0, 250)
            expected_party = deepcopy(party)
            _ = engine.get_play(party, "Mauvaka", 0)
            self.assertEqual(expected_party, party)
