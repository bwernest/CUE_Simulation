"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from .party import Party
from ..utils import *

# Python
from copy import deepcopy
import numpy as np
from numpy import argmin
from random import sample

"""___Classes___________________________________________________________________________________"""


class Game(Deck):

    score: NDArray
    turn: int
    round: int
    winner: Optional[int]

    min_energy: NDArray
    max_energy: NDArray
    resource_per_turn: Dict[Literal["power", "energy"], List[NDArray]]

    def create_game(
        self,
        deck_player: Deck,
        deck_opponent: Deck,
        start_energy: int,
        energy_per_turn: int,
        min_energy: int,
        max_energy: int,
    ) -> Party:
        """
        create_game
        -----------
        Initialisation d'une partie.

        Paramètres
        ----------
        deck_player : Deck
            Deck du joueur.
        deck_opponent : Deck
            Deck de l'adversaire.
        start_energy : int
            Energie de départ.
        energy_per_turn : int
            Energie par tour initiale.
        min_energy : int
            Energie minimum.
        max_energy : int
            Energie maximum.

        Retourne
        --------
        party : Party
            Instance de Party, état initial d'une partie.
        """
        party = Party()

        party.decks = [deck_player, deck_opponent]
        party.calculate_stats()

        party.energy = np.array([start_energy, start_energy])
        party.resource_per_turn = {
            "power": [np.zeros((7), dtype=int), np.zeros((7), dtype=int)],
            "energy": [np.zeros((7), dtype=int), np.zeros((7), dtype=int)]
        }
        party.resource_per_turn["energy"][0][0] = energy_per_turn
        party.resource_per_turn["energy"][1][0] = energy_per_turn
        party.min_energy = np.ones(2, dtype=int) * min_energy
        party.max_energy = np.ones(2, dtype=int) * max_energy
        party.score = np.zeros((self.rounds, self.turns, 2), dtype=int)
        party.turn = 0
        party.round = 0
        party.winner = None

        return party

    """___Play__________________________________________________________________________________"""

    def start_game(self, party: Party, shuffle: bool = True) -> None:
        self.stats = [self.get_stats(party.decks[0]), self.get_stats(party.decks[1])]
        if shuffle:
            for deck in party.decks:
                deck.shuffle()
        self.trigger_draw_attacks(party)
        self.trigger_start_attacks(party)

        party.decks[0].remaining = party.decks[0].order[:self.main_len]
        party.decks[1].remaining = party.decks[1].order[:self.main_len]

    def play(self, party: Party, play0: Play, play1: Play) -> None:
        plays = [play0, play1]
        self.turn_play(party, plays)
        self.turn_end(party, plays)
        self.turn_begin(party)

    def turn_begin(self, party: Party) -> None:
        self.trigger_draw_attacks(party)
        self.trigger_start_attacks(party)

    def turn_play(self, party: Party, plays: List[Play]) -> None:
        for player in range(2):
            party.decks[player].update_remaining(plays[player])

        self.play_attacks(party, plays)

        for player in range(2):
            carte_score = 0
            for k in range(self.play_len):
                if plays[player][k] is None:
                    continue
                carte = party.decks[player].cartes[plays[player][k]]  # type:ignore
                carte.played += 1
                carte_score += max(0, carte.base_power + np.sum(carte.buff["burn"]))
                carte_score += np.sum(carte.buff["power"])
                party.energy[player] -= max(0, carte.base_cost + np.sum(carte.buff["cost"]))
            power_per_turn = np.sum(party.resource_per_turn["power"][player])
            party.score[party.round, party.turn, player] += max(0, carte_score) + power_per_turn

    def play_attacks(self, party: Party, plays: List[Play]) -> None:
        for player in range(2):
            for k in range(self.play_len):
                if plays[player][k] is None:
                    continue
                self.trigger_attack(party, "play", plays, player, k)  # type:ignore

    def turn_end(self, party: Party, plays: List[Play]) -> None:
        for player in range(2):
            for k in range(self.play_len):
                if plays[player][k] is None:
                    continue
                self.trigger_attack(party, "return", plays, player, k)  # type:ignore
        self.add_energy_per_turn(party)
        self.debuff_cartes(party, plays)
        self.debuff_resources_per_turn(party)
        party.count_turn()
        for player in range(2):
            party.decks[player].cycle(plays[player])

    def add_energy_per_turn(self, party: Party) -> None:
        for player in range(2):
            party.energy[player] += np.sum(party.resource_per_turn["energy"][player])
        party.energy = np.clip(party.energy, party.min_energy, party.max_energy)

    def debuff_cartes(self, party: Party, plays) -> None:
        for player in range(2):
            for cid in party.decks[player].order:
                for data, buff in party.decks[player].cartes[cid].buff.items():
                    party.decks[player].cartes[cid].buff[data] = self.debuff_array(buff)
                    if cid in plays[player]:
                        party.decks[player].cartes[cid].buff[data][1] = 0

    def debuff_resources_per_turn(self, party: Party) -> None:
        for player in range(2):
            for data_per_turn, buff in party.resource_per_turn.items():
                party.resource_per_turn[data_per_turn][player] = self.debuff_array(buff[player])

    """___Attack________________________________________________________________________________"""

    def trigger_start_attacks(self, party: Party) -> None:
        for player in range(2):
            for carte in party.decks[player].main:
                for attack in party.decks[player].cartes[carte].attacks["start"]:
                    if self.check_conditions(party, attack["condition"], attack["acondition"], [], player, 26):
                        self.execute_attack(party, attack, carte, player)

    def trigger_draw_attacks(self, party: Party) -> None:
        for player in range(2):
            cartes_piochees = list(set(party.decks[player].main) - set(party.decks[player].remaining))
            for carte in cartes_piochees:
                for attack in party.decks[player].cartes[carte].attacks["draw"]:
                    if self.check_conditions(party, attack["condition"], attack["acondition"], [], player, 26):
                        self.execute_attack(party, attack, carte, player)

    def trigger_attack(self, party: Party, trigger: Literal["play", "return"], plays: List[List[str]], player: int, carte_index: int) -> None:
        carte = plays[player][carte_index]
        for attack in party.decks[player].cartes[carte].attacks[trigger]:
            if self.check_conditions(party, attack["condition"], attack["acondition"], plays, player, carte_index):
                self.execute_attack(party, attack, carte, player)

    def execute_attack(self, party: Party, attack: Dict, cid: str, player: int) -> None:
        targets = self.get_targets(party, attack["cible"], cid, player)
        for filtre in attack["filtre"]:
            targets = self.filter_targets(party, targets, filtre, player, cid)  # type:ignore
        for afiltre in attack["afiltre"]:
            atargets = self.filter_targets(party, deepcopy(targets), afiltre, player, cid)  # type:ignore
            for player in range(2):
                targets[player] = list(set(targets[player]) - set(atargets[player]))    # type:ignore
        self.apply_effects(party, attack["effet"], attack["multiplicateur"], attack["duree"], targets, player)

    """___Filtre________________________________________________________________________________"""

    def filter_targets(
        self,
        party: Party,
        targets: Dict[int, List[str]],
        atk_filtre: List,
        player: int,
        cid: str,
    ) -> Dict[int, List[str]]:
        try:
            return {
                "base_power": self.filter_targets_carte_attribut_amount,
                "base_cost": self.filter_targets_carte_attribut_amount,
                "rarity": self.filter_targets_carte_raritype,
                "type": self.filter_targets_carte_raritype,
                "random": self.filter_targets_random,
                "other": self.filter_targets_other,
            }[atk_filtre[0]](party, targets, atk_filtre, player, cid)
        except KeyError:
            raise FiltreKeyError(f"Filtre {atk_filtre[0]} inconnu")

    def filter_targets_carte_attribut_amount(
        self,
        party: Party,
        targets: Dict[int, List[str]],
        atk_filtre: List,
        player: int,
        cid: str,
    ) -> Dict[int, List[str]]:
        filtered_targets = {0: [], 1: []}
        for player in range(2):
            for cid in targets[player]:
                if self.check_condition_amount(atk_filtre[1], int(party.decks[player].cartes[cid].__getattribute__(atk_filtre[0])), int(atk_filtre[2])):
                    filtered_targets[player].append(cid)
        return filtered_targets

    def filter_targets_carte_raritype(
        self,
        party: Party,
        targets: Dict[int, List[str]],
        atk_filtre: List,
        player: int,
        cid: str,
    ) -> Dict[int, List[str]]:
        filtered_targets = {0: [], 1: []}
        for player in range(2):
            for cid in targets[player]:
                if party.decks[player].cartes[cid].__getattribute__(atk_filtre[0]) == atk_filtre[1]:
                    filtered_targets[player].append(cid)
        return filtered_targets

    def filter_targets_random(
        self,
        party: Party,
        targets: Dict[int, List],
        filtre: List,
        player: int,
        cid: str,
    ) -> Dict[int, List]:
        n_selected = int(filtre[1])
        len0, len1 = len(targets[0]), len(targets[1])
        if n_selected >= len0 + len1:
            return targets
        index_selected = sorted(sample([k for k in range(len0 + len1)], n_selected))
        selected = {}
        selected[0] = [targets[0][k] if k < len0 else None for k in index_selected]
        selected[1] = [targets[1][k - len0] if k >= len0 else None for k in index_selected]
        while None in selected[0]:
            selected[0].remove(None)
        while None in selected[1]:
            selected[1].remove(None)
        return selected

    def filter_targets_other(
        self,
        party: Party,
        targets: Dict[int, List[str]],
        atk_filtre: List,
        player: int,
        cid: str,
    ) -> Dict[int, List[str]]:
        targets[player].remove(cid)
        return targets

    """___Condition_____________________________________________________________________________"""

    def check_conditions(self, party: Party, conditions: List, aconditions: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        for atk_cdt in conditions:
            if not self.check_condition(party, atk_cdt, plays, player, carte_index):
                return False
        for atk_cdt in aconditions:
            if self.check_condition(party, atk_cdt, plays, player, carte_index):
                return False
        return True

    def check_condition(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        try:
            return {
                "player deck": self.check_condition_deck,
                "turn score": self.check_condition_turn_score,
                "round score": self.check_condition_round_score,
                "player played": self.check_condition_player_played,
                "player album": self.check_condition_player_album,
                "placement": self.check_condition_placement,
                "voisin": self.check_condition_voisin,
            }[atk_cdt[0]](party, atk_cdt, plays, player, carte_index)
        except KeyError:
            raise ConditionKeyError(f"Condition <{atk_cdt[0]}> inconnue")

    def check_condition_voisin(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        try:
            return {
                "gauche": self.check_condition_voisin_gauche,
                "droite": self.check_condition_voisin_droite,
                "next to": self.check_condition_voisin_next_to,
            }[atk_cdt[1]](party, atk_cdt, plays, player, carte_index)
        except KeyError:
            raise ConditionKeyError(f"Condition <{atk_cdt[1]}> inconnue")

    def check_condition_voisin_next_to(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        return {
            0: self.check_condition_voisin_droite,
            1: self.check_condition_voisin_gauche or self.check_condition_voisin_droite,
            2: self.check_condition_voisin_gauche,
        }[carte_index](party, atk_cdt, plays, player, carte_index)

    def check_condition_voisin_gauche(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        try:
            nei_carte = party.decks[player].cartes[plays[player][carte_index - 1]]
        except KeyError:
            return atk_cdt[2] == "vide"
        return atk_cdt[2] != "vide" and nei_carte.__getattribute__(atk_cdt[2]) == atk_cdt[3]

    def check_condition_voisin_droite(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        try:
            nei_carte = party.decks[player].cartes[plays[player][carte_index + 1]]
        except KeyError:
            return atk_cdt[2] == "vide"
        return atk_cdt[2] != "vide" and nei_carte.__getattribute__(atk_cdt[2]) == atk_cdt[3]

    def check_condition_placement(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        try:
            return {
                "gauche": 0,
                "milieu": 1,
                "droite": 2,
            }[atk_cdt[1]] == carte_index
        except KeyError:
            raise ConditionKeyError(f"Condition <{atk_cdt[1]}> inconnue")

    def check_condition_player_album(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        amount_player = len(party.stats[player]["album"])
        return self.check_condition_amount(atk_cdt[1], amount_player, int(atk_cdt[2]))

    def check_condition_deck(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        try:
            return {
                "name": self.check_condition_deck_carte,
                "collection": self.check_condition_deck_set,
                "album": self.check_condition_deck_set,
            }[atk_cdt[1]](party, atk_cdt, plays, player, carte_index)
        except KeyError:
            raise ConditionKeyError(f"Condition <{atk_cdt[1]}> inconnue")

    def check_condition_deck_carte(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        try:
            _ = party.decks[player].name_to_id[atk_cdt[2]]
        except KeyError:
            return False
        return True

    def check_condition_deck_set(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        amount_deck = self.get_amount(party, player, atk_cdt[1], atk_cdt[2])
        amount_target = int(atk_cdt[4])
        return self.check_condition_amount(atk_cdt[3], amount_deck, amount_target)

    def check_condition_turn_score(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        amount_turn_score = party.score[party.round, party.turn, player] - party.score[party.round, party.turn, 1 - player]
        amount_target = int(atk_cdt[2])
        return self.check_condition_amount(atk_cdt[1], amount_turn_score, amount_target)

    def check_condition_round_score(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        amount_round_score = np.sum(party.score[party.round, :, player]) - np.sum(party.score[party.round, :, 1 - player])
        amount_target = int(atk_cdt[2])
        return self.check_condition_amount(atk_cdt[1], amount_round_score, amount_target)

    def check_condition_player_played(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        try:
            return {
                "name": self.check_condition_played_carte,
                "collection": self.check_condition_played_deck,
                "album": self.check_condition_played_deck,
                "keyword": self.check_condition_played_keyword,
            }[atk_cdt[1]](party, atk_cdt, plays, player, carte_index)
        except KeyError:
            raise ConditionKeyError(f"Condition <{atk_cdt[1]}> inconnue")

    def check_condition_played_carte(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> bool:
        try:
            cid = party.decks[player].name_to_id[atk_cdt[2]]
            amount_played = party.decks[player].cartes[cid].played
        except KeyError:
            amount_played = 0
        return self.check_condition_amount(">", amount_played, 0)

    def check_condition_played_deck(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> int:
        amount_played = 0
        for carte in party.decks[player].cartes.values():
            if carte.__getattribute__(atk_cdt[1]) == atk_cdt[2]:
                amount_played += carte.played
        return self.check_condition_amount(atk_cdt[3], amount_played, int(atk_cdt[4]))

    def check_condition_played_keyword(self, party: Party, atk_cdt: List, plays: List[List[str]], player: int, carte_index: int) -> int:
        amount_played = 0
        for carte in party.decks[player].cartes.values():
            if atk_cdt[2] in carte.keywords:
                amount_played += carte.played
        return self.check_condition_amount(atk_cdt[3], amount_played, int(atk_cdt[4]))

    def check_condition_amount(self, comparaison: str, amount_player: int, amount_target: int) -> bool:
        try:
            return {
                "<": self.check_condition_amount_lt,
                ">": self.check_condition_amount_gt,
                "=": self.check_condition_amount_eq,
            }[comparaison](amount_player, amount_target)
        except KeyError:
            raise ComparaisonKeyError(f"Comparaison {comparaison} inconnue")

    def get_amount(self, party: Party, player: int, set_type: str, set_name: str) -> int:
        try:
            return party.stats[player][set_type][set_name]
        except KeyError:
            return 0

    def check_condition_amount_lt(self, amount_player: int, amount_target: int) -> bool:
        return amount_player < amount_target

    def check_condition_amount_gt(self, amount_player: int, amount_target: int) -> bool:
        return amount_player > amount_target

    def check_condition_amount_eq(self, amount_player: int, amount_target: int) -> bool:
        return amount_player == amount_target

    """___Target________________________________________________________________________________"""

    def get_targets(self, party: Party, target_attacks: List, carte: str, player: int) -> Dict[int, List[str | int]]:
        """
        Attention si la cible est un joueur
        """
        targets = {0: [], 1: []}
        for target_attack in target_attacks:
            target = self.get_target(party, target_attack, carte, player)
            for joueur in range(2):
                targets[joueur] += target[joueur]
        targets[0] = list(set(targets[0]))
        targets[1] = list(set(targets[1]))
        return targets

    def get_target(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str | int]]:
        try:
            return {
                "self": self.get_target_self,
                "player": self.get_target_player,
                "opponent": self.get_target_opponent,
                "player main": self.get_target_player_main,
                "player deck": self.get_target_player_deck,
                "player remaining": self.get_target_player_remaining,
                "opponent main": self.get_target_opponent_main,
                "opponent deck": self.get_target_opponent_deck,
                "opponent remaining": self.get_target_opponent_remaining,
                "both main": self.get_target_both_main,
                "both deck": self.get_target_both_deck,
                "both remaining": self.get_target_both_remaining,
            }[target_attack[0]](party, target_attack, carte, player)
        except KeyError:
            raise TargetKeyError(f"Target {target_attack} inconnue")

    def get_target_self(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str]]:
        return {player: [carte], 1 - player: []}

    def get_target_player(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[int]]:
        return {player: [player], 1 - player: []}

    def get_target_opponent(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[int]]:
        return {player: [1 - player], 1 - player: []}

    def get_target_player_main(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cartes(party, target_attack, player, "main")

    def get_target_player_deck(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cartes(party, target_attack, player, "order")

    def get_target_player_remaining(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cartes(party, target_attack, player, "remaining")

    def get_target_opponent_main(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cartes(party, target_attack, 1 - player, "main")

    def get_target_opponent_deck(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cartes(party, target_attack, 1 - player, "order")

    def get_target_opponent_remaining(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cartes(party, target_attack, 1 - player, "remaining")

    def get_target_both_main(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str]]:
        targets = {}
        targets[player] = self.get_target_cartes(party, target_attack, player, "main")[player]
        targets[1 - player] = self.get_target_cartes(party, target_attack, 1 - player, "main")[1 - player]
        return targets

    def get_target_both_deck(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str]]:
        targets = {}
        targets[player] = self.get_target_cartes(party, target_attack, player, "order")[player]
        targets[1 - player] = self.get_target_cartes(party, target_attack, 1 - player, "order")[1 - player]
        return targets

    def get_target_both_remaining(self, party: Party, target_attack: List, carte: str, player: int) -> Dict[int, List[str]]:
        dict0 = self.get_target_cartes(party, target_attack, player, "remaining")
        dict1 = self.get_target_cartes(party, target_attack, 1 - player, "remaining")
        return self.merge_dict(dict0, dict1)

    def get_target_cartes(
        self,
        party: Party,
        atk_target: List,
        player_targeted: int,
        location: Literal["main", "order", "remaining"],
    ) -> Dict[int, List[str]]:
        # N'importe
        if len(atk_target) == 1:
            targets = {0: [], 1: []}
            targets[player_targeted] = party.decks[player_targeted].__getattribute__(location)
            return targets
        # Collection ou Album spécifique
        else:
            return {
                "name": self.get_target_cartes_carte,
                "collection": self.get_target_cartes_deck,
                "album": self.get_target_cartes_deck,
                "keyword": self.get_target_cartes_keyword,
            }[atk_target[1]](party, atk_target, player_targeted, location)

    def get_target_cartes_carte(
        self,
        party: Party,
        atk_target: List,
        player_targeted: int,
        location: Literal["main", "order", "remaining"],
    ) -> Dict:
        targets = {0: [], 1: []}
        try:
            cid_targeted = party.decks[player_targeted].name_to_id[atk_target[2]]
        except KeyError:
            return targets
        if cid_targeted in party.decks[player_targeted].__getattribute__(location):
            targets[player_targeted].append(cid_targeted)
            return targets
        return targets

    def get_target_cartes_deck(
        self,
        party: Party,
        atk_target: List,
        player_targeted: int,
        location: Literal["main", "order", "remaining"],
    ) -> Dict:
        targets = {0: [], 1: []}
        for cid in party.decks[player_targeted].__getattribute__(location):
            if party.decks[player_targeted].cartes[cid].__getattribute__(atk_target[1]) == atk_target[2]:
                targets[player_targeted].append(cid)
        return targets

    def get_target_cartes_keyword(
        self,
        party: Party,
        atk_target: List,
        player_targeted: int,
        location: Literal["main", "order", "remaining"],
    ) -> Dict:
        targets = {0: [], 1: []}
        for cid in party.decks[player_targeted].__getattribute__(location):
            if atk_target[2] in party.decks[player_targeted].cartes[cid].keywords:
                targets[player_targeted].append(cid)
        return targets

    """___Effect________________________________________________________________________________"""

    def apply_effects(
        self,
        party: Party,
        atk_effect: List,
        atk_mult: List,
        atk_duree: List,
        targets: Dict[int, List],
        player: int,
    ) -> None:
        try:
            {
                "power": self.apply_effect_carte,
                "burn": self.apply_effect_carte,
                "cost": self.apply_effect_carte,
                "lock": self.apply_effect_carte_lock,
                "energy": self.apply_effect_energy,
                "power per turn": self.apply_effect_resource_per_turn,
                "energy per turn": self.apply_effect_resource_per_turn,
            }[atk_effect[0]](party, atk_effect, atk_mult, atk_duree, targets, player)
        except KeyError:
            raise EffectKeyError(f"Effect <{atk_effect[0]}> inconnu")

    def apply_effect_carte(
        self,
        party: Party,
        atk_effect: List,
        atk_mult: List,
        atk_duree: List,
        targets: Dict[int, List],
        player: int,
    ) -> None:
        index = self.get_index_from_duree(party, atk_duree)
        mult = 1 if atk_mult == [] else self.get_multiplicateur(party, atk_mult, player)
        for player in range(2):
            for carte in targets[player]:
                party.decks[player].cartes[carte].buff[atk_effect[0]][index] += int(atk_effect[1]) * mult

    def apply_effect_carte_lock(
        self,
        party: Party,
        atk_effect: List,
        atk_mult: List,
        atk_duree: List,
        targets: Dict[int, List],
        player: int,
    ) -> None:
        index = self.get_index_from_duree(party, atk_duree)
        for player in range(2):
            for carte in targets[player]:
                party.decks[player].cartes[carte].buff[atk_effect[0]][2:index + 1] = [1] * (index - 2 + 1)

    def apply_effect_resource_per_turn(
        self,
        party: Party,
        atk_effect: List,
        atk_mult: List,
        atk_duree: List,
        targets: Dict[int, List],
        player: int,
    ) -> None:
        data = atk_effect[0][:-9]
        player_targeted = targets[player][0]
        amount = int(atk_effect[1])
        index = self.get_index_from_duree(party, atk_duree)
        mult = 1 if atk_mult == [] else self.get_multiplicateur(party, atk_mult, player)
        party.resource_per_turn[data][player_targeted][index] += amount * mult

    def get_index_from_duree(self, party: Party, duree: List) -> int:
        try:
            return {
                "turn": int(duree[1]) + 1,
                "round": int(duree[1]) * 3 - party.turn + 1,
                "until played": 1,
                "permanently": 0,
            }[duree[0]]
        except IndexError:
            return {
                "until played": 1,
                "permanently": 0,
            }[duree[0]]
        except KeyError:
            raise DureeKeyError(f"Durée {duree[0]} inconnue")

    def apply_effect_energy(
        self,
        party: Party,
        atk_effect: List,
        atk_mult: List,
        atk_duree: List,
        targets: Dict[int, List],
        player: int,
    ) -> None:
        party.energy[targets[player][0]] += int(atk_effect[1])

    """___Multiplicateur________________________________________________________________________"""

    def get_multiplicateur(self, party: Party, attack_mult: List, player: int) -> int:
        try:
            return {
                "player main": self.get_multiplicateur_main,
                "player deck": self.get_multiplicateur_deck,
                "player played": self.get_multiplicateur_played,
                "player album": self.get_multiplicateur_album,
                "round completed": self.get_multiplicateur_round_completed,
                "both deck": self.get_multiplicateur_both_deck,
            }[attack_mult[0]](party, attack_mult, player)
        except KeyError:
            raise MultiplicateurKeyError(f"Multiplicateur <{attack_mult[0]}> inconnue")

    def get_multiplicateur_main(self, party: Party, attack_mult: List, player: int) -> int:
        multiplicateur = 0
        for cid in party.decks[player].main:
            if party.decks[player].cartes[cid].__getattribute__(attack_mult[1]) == attack_mult[2]:
                multiplicateur += 1
        return self.get_maxed_multiplicateur(multiplicateur, attack_mult, 3)

    def get_multiplicateur_deck(self, party: Party, attack_mult: List, player: int) -> int:
        try:
            return self.get_maxed_multiplicateur(party.stats[player][attack_mult[1]][attack_mult[2]], attack_mult, 3)
        except KeyError:
            return 0

    def get_multiplicateur_played(self, party: Party, attack_mult: List, player: int) -> int:
        try:
            return self.get_maxed_multiplicateur({
                "name": self.get_multiplicateur_played_carte,
                "collection": self.get_multiplicateur_played_deck,
                "album": self.get_multiplicateur_played_deck,
            }[attack_mult[1]](party, attack_mult, player), attack_mult, 3)
        except KeyError:
            raise MultiplicateurKeyError(f"Multiplicateur <{attack_mult[1]}> inconnue")

    def get_multiplicateur_album(self, party: Party, attack_mult: List, player: int) -> int:
        return len(party.stats[player]["album"])

    def get_multiplicateur_played_carte(self, party: Party, attack_mult: List, player: int) -> int:
        try:
            cid = party.decks[player].name_to_id[attack_mult[2]]
        except KeyError:
            raise CarteAbsenteDuDeck()
        return party.decks[player].cartes[cid].played

    def get_multiplicateur_played_deck(self, party: Party, attack_mult: List, player: int) -> int:
        multiplicateur = 0
        for carte in party.decks[player].cartes.values():
            if carte.__getattribute__(attack_mult[1]) == attack_mult[2]:
                multiplicateur += carte.played
        return multiplicateur

    def get_multiplicateur_round_completed(self, party: Party, attack_mult: List, player: int) -> int:
        return party.round

    def get_multiplicateur_both_deck(self, party: Party, atk_mult: List, player: int) -> int:
        mult_player0 = self.get_multiplicateur_played_deck(party, atk_mult, 0)
        mult_player1 = self.get_multiplicateur_played_deck(party, atk_mult, 1)
        return mult_player0 + mult_player1

    def get_maxed_multiplicateur(self, multiplicateur: int, attack_mult: List, index: int) -> int:
        try:
            return min(multiplicateur, int(attack_mult[index]))
        except IndexError:
            return multiplicateur

    """___Miscellaneous_________________________________________________________________________"""
