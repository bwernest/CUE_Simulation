"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .asserts import Assert
from ..engine.engine import Engine
from .fixtures import *
from ..utils.errors import *
from . import *
import numpy as np

# Python
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestEngine(Assert):

    @void
    def test_settings(self) -> None:
        with pytest.raises(SettingsNotAvailable):
            _ = Engine("deltaplane")

    def test_addition(self, engine: Engine) -> None:
        expected = 2
        result = engine.addition(1, 1)
        self.assertEqual(expected, result)
