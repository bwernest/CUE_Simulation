"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from . import *
from ..engine.carte import Carte
from ..engine.engine import Engine

# Python
import numpy as np
import pytest

"""___Tests_____________________________________________________________________________________"""


class TestCarte(Assert):

    def test_create_carte(self) -> None:
        _ = Carte("test")

    def test_carte_import(self, engine: Engine) -> None:
        carte = engine.cartes["mypa001"]
        self.assertEqual(["2020"], carte.keywords)

    def test_carte_equal(self, engine: Engine) -> None:
        expected = True
        carte1 = engine.cartes["mypa001"]
        carte2 = engine.cartes["mypa001"]
        result = carte1 == carte2
        self.assertEqual(expected, result)

    def test_carte_not_equal1(self, engine: Engine) -> None:
        expected = False
        carte1 = engine.cartes["mypa001"]
        carte2 = engine.cartes["pan015"]
        result = carte1 == carte2
        self.assertEqual(expected, result)

    def test_carte_not_equal2(self, engine: Engine) -> None:
        expected = False
        carte1 = engine.cartes["pan015"]
        result = carte1 == engine
        self.assertEqual(expected, result)
