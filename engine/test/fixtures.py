"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..engine.engine import Engine

# Python
import pytest

"""___Functions_________________________________________________________________________________"""


@pytest.fixture(scope="class")
def engine() -> Engine:
    engine = Engine("test")
    return engine
