"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.engine import Engine

# Python
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestEngine(Assert):

    @void
    def test_settings(self) -> None:
        with pytest.raises(SettingsNotAvailable):
            _ = Engine("deltaplane")
