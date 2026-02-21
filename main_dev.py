"""___Notes_________________________________________________________________"""
"""
- Parsing pré game pour désactiver les attaques non activables
- Parsing pré game pour compter le nombres de cartes de chaque type (opti attaques)
- Contrôle : effet return sur le round, se termine juste maintenant
- Les effets return sont DANS le tour, et ensuite décompte du tour
- But de l'hiver : trier les cartes par interet
    -> Fonction selection qui a une carte calcule un score
- Tests d'un play à une carte (centrosaurus)
"""
"""___Modules_______________________________________________________________"""

# CUE_Simulation
from engine.engine.engine import Engine

"""___Execution_____________________________________________________________"""

engine = Engine("prod")
engine.start()
print(engine.game.score)
