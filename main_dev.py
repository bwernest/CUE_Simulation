"""___Notes_________________________________________________________________"""
"""
___Optimisation___
- Parsing pré game pour désactiver les attaques non activables
- Parsing pré game pour compter le nombres de cartes de chaque type (opti attaques)
- Classe Game qui récupère un dico, un play et donne le suivant
- Pour le typing certains 'range(2)' ont été remplacés par des 'get_args(JoueurID)'

___BaffWill___
- But de l'hiver : trier les cartes par interet
    -> Fonction selection qui a une carte calcule un score
- Dev de la classe Party pour gérer le Monte Carlo

___Jeu___
- Contrôle : effet return sur le round, se termine juste maintenant
- On draw, le burn affecte d'un tick les cartes adverses (hellboy)

___IA___
- Coder plusieurs IA qui s'affronteront :
    - Mallia : Jouer au hasard
    - Mauvaka : Maximiser le power au tour T
    - Marchand : Maximiser le power à la fin du round
    - Novès :   Maximiser le power total du deck au tour T
    - Mola :    Maximiser le power total du deck au tour T+1
    - Lacroix : Maximiser le power total du deck au tour T+2
    
    - Ramos :   Novès puis Marchand à X-2
    - Ntamack : Mola puis Marchand à X-2
    - Dupont :  Lacroix puis Marchand à X-2
    - Lebel :   Novès puis Marchand à 2-X
    - Capuozzo : Mola puis Marchand à 2-X
    - Kinghorn :  Lacroix puis Marchand à 2-X
    - Jelonch : Novès puis Mauvaka à X-2
    - Willis : Mola puis Mauvaka à X-2
    - Meafou : Lacroix puis Mauvaka à X-2
    - Graou : Novès puis Mauvaka à 2-X
    - Barassi : Mola puis Mauvaka à 2-X
    - Ahki : Lacroix puis Mauvaka à 2-X
"""
"""___Modules_______________________________________________________________"""

# CUE_Simulation
from engine.engine.carte import Carte
from engine.engine.deck import Deck
from engine.engine.engine import Engine
from engine.engine.party import Party
from engine.test.fixtures import dummy_deck
from engine.utils import *

"""___Fonctions_____________________________________________________________"""


def test_cartes_all() -> None:
    engine = Engine("prod")
    engine.start_engine(recyclage=True)
    for cid in engine.cartes.keys():
        print(f"Test de {engine.cartes[cid].name}")
        for placement in range(3):
            deck0 = dummy_deck()
            deck1 = dummy_deck()
            deck0.replace_carte("id0", engine.cartes[cid])
            party = engine.create_game(deck0, deck1, 100, 0, 0, 250)
            engine.start_game(party, shuffle=False)
            play0: List[Any] = [None, None, None]
            play0[placement] = cid
            engine.play(party, play0, [None, None, None])


"""___Execution_____________________________________________________________"""

engine = Engine("prod")
engine.start_engine()

player_deck = Deck("prod")
player_deck.create_deck([engine.cartes[cid] for cid in deck_list_grodino])
opponent_deck = Deck("prod")
opponent_deck.create_deck([engine.cartes[cid] for cid in deck_list_grodino])

for _ in range(10):
    party = engine.fight(player_deck, opponent_deck, "Mauvaka", "Mauvaka")
    party.show_score()

# test_cartes_all()
