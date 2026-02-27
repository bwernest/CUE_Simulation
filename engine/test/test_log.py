"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .asserts import Assert
from ..engine.engine import Engine
from .fixtures import *

"""___Tests_____________________________________________________________________________________"""


class TestLog(Assert):

    def test_writing(self, engine: Engine) -> None:
        engine.add_log("Not quite my tempo")
        engine.del_log()
