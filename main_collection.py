"""___Modules_______________________________________________________________"""

# CUE_Simulation
from engine.engine.engine import Engine
from engine.engine.game import Game
from engine.test.fixtures import dummy_deck

"""___Execution_____________________________________________________________"""

engine = Engine("prod")
engine.start_engine()

engine.rewrite_raw_data()

engine.print_cartes_albums()
engine.print_cartes_collections()
engine.print_collection("herbivores")
