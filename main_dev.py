"""___Notes_________________________________________________________________"""
"""
blablabla
"""
"""___Modules_______________________________________________________________"""

# CUE_Simulation
from engine.engine.engine import Engine

"""___Execution_____________________________________________________________"""

engine = Engine("prod")
engine.start()
print(engine.game.score)
