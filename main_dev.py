"""___Notes_________________________________________________________________"""
"""
- Parsing pré game pour désactiver les attaques non activables
- Parsing pré game pour compter le nombres de cartes de chaque type (opti attaques)
- Contrôle : effet return sur le round, se termine juste maintenant
- But de l'hiver : trier les cartes par interet
    -> Fonction selection qui a une carte calcule un score
- Tests d'un play à une carte (centrosaurus)
- On draw, le burn affecte d'un tick les cartes adverses (hellboy)
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
from engine.engine.engine import Engine
from engine.engine.game import Game
from engine.test.fixtures import dummy_deck

"""___Fonctions_____________________________________________________________"""


def unique_card_play(card_id: str) -> Game:
    engine = Engine("test")
    engine.start_engine()
    deck1 = dummy_deck()
    deck2 = dummy_deck()
    card_id = card_id.lower()
    deck1.replace_card("id0", engine.cards[card_id])
    engine.start_game(deck1, deck2, 100, 0, 0, 250, shuffle=False)
    engine.play([card_id, None, None], [None, None, None])
    return engine.game


def test_card_all() -> None:
    engine = Engine("prod")
    engine.start_engine()
    for card_id in engine.cards.keys():
        print(f"Test de {engine.cards[card_id].name}")
        deck0 = dummy_deck()
        deck1 = dummy_deck()
        deck0.replace_card("id0", engine.cards[card_id])
        engine.start_game(deck0, deck1, 100, 0, 0, 250, shuffle=False)


"""___Execution_____________________________________________________________"""

engine = Engine("prod")
engine.start_engine()
# engine.print_check_raw_cards()
engine.rewrite_raw_data()
engine.print_cards_collections()
engine.print_collection("omnivores")
# test_card_all()
