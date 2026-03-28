"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from ..utils import *

# Python
import numpy as np
from numpy.typing import NDArray
from typing import Dict, List, Literal

"""___Classes___________________________________________________________________________________"""


class Game(Deck):

    decks: List[Deck]

    score: NDArray
    turn: int
    round: int
    winner: int | None

    min_energy: NDArray
    max_energy: NDArray

    def create_game(
            self,
            deck0: Deck,
            deck1: Deck,
            start_energy: int,
            energy_per_turn: int,
            min_energy: int,
            max_energy: int,
    ) -> None:
        self.decks = [deck0, deck1]
        self.energy = np.array([start_energy, start_energy])
        self.resource_per_turn = {
            "power": [np.zeros((7), dtype=int), np.zeros((7), dtype=int)],
            "energy": [np.zeros((7), dtype=int), np.zeros((7), dtype=int)]
        }
        self.resource_per_turn["energy"][0][0] = energy_per_turn
        self.resource_per_turn["energy"][1][0] = energy_per_turn
        self.min_energy = np.ones(2, dtype=int) * min_energy
        self.max_energy = np.ones(2, dtype=int) * max_energy
        self.score = np.zeros((self.rounds, self.turns, 2), dtype=int)
        self.turn = 0
        self.round = 0
        self.winner = None
        self.stats = [self.get_stats(deck0), self.get_stats(deck1)]

    """___Play__________________________________________________________________________________"""

    def start_game(self, shuffle: bool = True) -> None:
        if shuffle:
            for deck in self.decks:
                deck.shuffle()
        self.trigger_draw_attacks()
        self.trigger_start_attacks()

        self.decks[0].remaining = self.decks[0].order[:self.hand_len]
        self.decks[1].remaining = self.decks[1].order[:self.hand_len]

    def play(self, play0: List[str | None], play1: List[str | None]) -> None:
        plays = [play0, play1]
        self.turn_play(plays)
        self.turn_end(plays)
        self.turn_begin()

    def turn_begin(self) -> None:
        self.trigger_draw_attacks()
        self.trigger_start_attacks()

    def turn_play(self, plays: List[List[str | None]]) -> None:
        for player in range(2):
            self.decks[player].update_remaining(plays[player])

        self.play_attacks(plays)

        for player in range(2):
            card_score = 0
            for k in range(self.play_len):
                if plays[player][k] is None:
                    continue
                card = self.decks[player].cards[plays[player][k]]  # type:ignore
                card.played += 1
                card_score += max(0, card.base_power + np.sum(card.buff["burn"]))
                card_score += np.sum(card.buff["power"])
                self.energy[player] -= max(0, card.base_cost + np.sum(card.buff["cost"]))
            power_per_turn = np.sum(self.resource_per_turn["power"][player])
            self.score[self.round, self.turn, player] += max(0, card_score) + power_per_turn

    def play_attacks(self, plays: List[List[str | None]]) -> None:
        for player in range(2):
            for k in range(self.play_len):
                if plays[player][k] is None:
                    continue
                self.trigger_attack("play", plays, player, k)  # type:ignore

    def turn_end(self, plays: List[List[str | None]]) -> None:
        for player in range(2):
            for k in range(self.play_len):
                if plays[player][k] is None:
                    continue
                self.trigger_attack("return", plays, player, k)  # type:ignore
        self.add_energy_per_turn()
        self.debuff_cards(plays)
        self.debuff_resources_per_turn()
        self.count_turn()
        for player in range(2):
            self.decks[player].cycle(plays[player])

    def add_energy_per_turn(self) -> None:
        for player in range(2):
            self.energy[player] += np.sum(self.resource_per_turn["energy"][player])
        self.energy = np.clip(self.energy, self.min_energy, self.max_energy)

    def debuff_cards(self, plays) -> None:
        for player in range(2):
            for card_id in self.decks[player].order:
                for data, buff in self.decks[player].cards[card_id].buff.items():
                    self.decks[player].cards[card_id].buff[data] = self.debuff_array(buff)
                    if card_id in plays[player]:
                        self.decks[player].cards[card_id].buff[data][1] = 0

    def debuff_resources_per_turn(self) -> None:
        for player in range(2):
            for data_per_turn, buff in self.resource_per_turn.items():
                self.resource_per_turn[data_per_turn][player] = self.debuff_array(buff[player])

    """___Attack________________________________________________________________________________"""

    def trigger_start_attacks(self) -> None:
        for player in range(2):
            for card in self.decks[player].hand:
                for attack in self.decks[player].cards[card].attacks["start"]:
                    if self.check_conditions(attack["condition"], attack["acondition"], [], player, 26):
                        self.execute_attack(attack, card, player)

    def trigger_draw_attacks(self) -> None:
        for player in range(2):
            cards_drawn = list(set(self.decks[player].hand) - set(self.decks[player].remaining))
            for card in cards_drawn:
                for attack in self.decks[player].cards[card].attacks["draw"]:
                    if self.check_conditions(attack["condition"], attack["acondition"], [], player, 26):
                        self.execute_attack(attack, card, player)

    def trigger_attack(self, trigger: Literal["play", "return"], plays: List[List[str]], player: int, card_index: int) -> None:
        card = plays[player][card_index]
        for attack in self.decks[player].cards[card].attacks[trigger]:
            if self.check_conditions(attack["condition"], attack["acondition"], plays, player, card_index):
                self.execute_attack(attack, card, player)

    def execute_attack(self, attack: Dict, card_id: str, player: int) -> None:
        targets = self.get_targets(attack["cible"], card_id, player)
        if attack["filtre"] != []:
            for filtre in attack["filtre"]:
                targets = self.filter_targets(targets, filtre, player, card_id)  # type:ignore
        self.apply_effects(attack["effet"], attack["multiplicateur"], attack["duree"], targets, player)

    """___Filtre________________________________________________________________________________"""

    def filter_targets(
        self,
        targets: Dict[int, List[str]],
        atk_filtre: List,
        player: int,
        card_id: str,
    ) -> Dict[int, List[str]]:
        try:
            return {
                "base_power": self.filter_targets_card_attribut_amount,
                "base_cost": self.filter_targets_card_attribut_amount,
                "rarity": self.filter_targets_card_rarity,
                "random": self.filter_targets_random,
                "other": self.filter_targets_other,
            }[atk_filtre[0]](targets, atk_filtre, player, card_id)
        except KeyError:
            raise FiltreKeyError(f"Filtre {atk_filtre[0]} inconnu")

    def filter_targets_card_attribut_amount(
        self,
        targets: Dict[int, List[str]],
        atk_filtre: List,
        player: int,
        card_id: str,
    ) -> Dict[int, List[str]]:
        filtered_targets = {0: [], 1: []}
        for player in range(2):
            for card_id in targets[player]:
                if self.check_condition_amount(atk_filtre[1], int(self.decks[player].cards[card_id].__getattribute__(atk_filtre[0])), int(atk_filtre[2])):
                    filtered_targets[player].append(card_id)
        return filtered_targets

    def filter_targets_card_rarity(
        self,
        targets: Dict[int, List[str]],
        atk_filtre: List,
        player: int,
        card_id: str,
    ) -> Dict[int, List[str]]:
        filtered_targets = {0: [], 1: []}
        for player in range(2):
            for card_id in targets[player]:
                if self.decks[player].cards[card_id].rarity == atk_filtre[1]:
                    filtered_targets[player].append(card_id)
        return filtered_targets

    def filter_targets_other(
        self,
        targets: Dict[int, List[str]],
        atk_filtre: List,
        player: int,
        card_id: str,
    ) -> Dict[int, List[str]]:
        targets[player].remove(card_id)
        return targets

    """___Condition_____________________________________________________________________________"""

    def check_conditions(self, conditions: List, aconditions: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        for atk_cdt in conditions:
            if not self.check_condition(atk_cdt, plays, player, card_index):
                return False
        for atk_cdt in aconditions:
            if self.check_condition(atk_cdt, plays, player, card_index):
                return False
        return True

    def check_condition(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        try:
            return {
                "player deck": self.check_condition_deck,
                "turn score": self.check_condition_turn_score,
                "round score": self.check_condition_round_score,
                "player played": self.check_condition_player_played,
                "player album": self.check_condition_player_album,
                "placement": self.check_condition_placement,
                "voisin": self.check_condition_voisin,
            }[atk_cdt[0]](atk_cdt, plays, player, card_index)
        except KeyError:
            raise ConditionKeyError(f"Condition <{atk_cdt[0]}> inconnue")

    def check_condition_voisin(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        return {
            "gauche": self.check_condition_voisin_gauche,
            "droite": self.check_condition_voisin_droite,
            "next to": self.check_condition_voisin_next_to,
        }[atk_cdt[1]](atk_cdt, plays, player, card_index)

    def check_condition_voisin_next_to(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        return {
            0: self.check_condition_voisin_droite,
            1: self.check_condition_voisin_gauche or self.check_condition_voisin_droite,
            2: self.check_condition_voisin_gauche,
        }[card_index](atk_cdt, plays, player, card_index)

    def check_condition_voisin_gauche(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        try:
            nei_card = self.decks[player].cards[plays[player][card_index - 1]]
        except KeyError:
            return atk_cdt[2] == "vide"
        return atk_cdt[2] != "vide" and nei_card.__getattribute__(atk_cdt[2]) == atk_cdt[3]

    def check_condition_voisin_droite(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        try:
            nei_card = self.decks[player].cards[plays[player][card_index + 1]]
        except KeyError:
            return atk_cdt[2] == "vide"
        return atk_cdt[2] != "vide" and nei_card.__getattribute__(atk_cdt[2]) == atk_cdt[3]

    def check_condition_placement(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        return {
            "gauche": 0,
            "milieu": 1,
            "droite": 2,
        }[atk_cdt[1]] == card_index

    def check_condition_player_album(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        amount_player = len(self.stats[player]["album"])
        return self.check_condition_amount(atk_cdt[1], amount_player, int(atk_cdt[2]))

    def check_condition_deck(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        return {
            "name": self.check_condition_deck_card,
            "collection": self.check_condition_deck_set,
            "album": self.check_condition_deck_set,
        }[atk_cdt[1]](atk_cdt, plays, player, card_index)

    def check_condition_deck_card(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        try:
            _ = self.decks[player].name_to_id[atk_cdt[2]]
        except KeyError:
            return False
        return True

    def check_condition_deck_set(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        amount_deck = self.get_amount(player, atk_cdt[1], atk_cdt[2])
        amount_target = int(atk_cdt[4])
        return self.check_condition_amount(atk_cdt[3], amount_deck, amount_target)

    def check_condition_turn_score(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        amount_turn_score = self.score[self.round, self.turn, player] - self.score[self.round, self.turn, 1 - player]
        amount_target = int(atk_cdt[2])
        return self.check_condition_amount(atk_cdt[1], amount_turn_score, amount_target)

    def check_condition_round_score(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        amount_round_score = np.sum(self.score[self.round, :, player]) - np.sum(self.score[self.round, :, 1 - player])
        amount_target = int(atk_cdt[2])
        return self.check_condition_amount(atk_cdt[1], amount_round_score, amount_target)

    def check_condition_player_played(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        return {
            "name": self.check_condition_played_card,
            "collection": self.check_condition_played_deck,
            "album": self.check_condition_played_deck,
        }[atk_cdt[1]](atk_cdt, player)

    def check_condition_played_card(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> bool:
        try:
            card_id = self.decks[player].name_to_id[atk_cdt[2]]
        except KeyError:
            raise CarteAbsenteDuDeck()
        amount_played = self.decks[player].cards[card_id].played
        return self.check_condition_amount(atk_cdt[3], amount_played, int(atk_cdt[4]))

    def check_condition_played_deck(self, atk_cdt: List, plays: List[List[str]], player: int, card_index: int) -> int:
        amount_played = 0
        for card in self.decks[player].cards.values():
            if card.__getattribute__(atk_cdt[1]) == atk_cdt[2]:
                amount_played += card.played
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

    def get_amount(self, player: int, set_type: str, set_name: str) -> int:
        try:
            return self.stats[player][set_type][set_name]
        except KeyError:
            return 0

    def check_condition_amount_lt(self, amount_player: int, amount_target: int) -> bool:
        return amount_player < amount_target

    def check_condition_amount_gt(self, amount_player: int, amount_target: int) -> bool:
        return amount_player > amount_target

    def check_condition_amount_eq(self, amount_player: int, amount_target: int) -> bool:
        return amount_player == amount_target

    """___Target________________________________________________________________________________"""

    def get_targets(self, target_attacks: List, card: str, player: int) -> Dict[int, List[str | int]]:
        """
        Attention si la cible est un joueur
        """
        targets = {0: [], 1: []}
        for target_attack in target_attacks:
            target = self.get_target(target_attack, card, player)
            for joueur in range(2):
                targets[joueur] += target[joueur]
        targets[0] = list(set(targets[0]))
        targets[1] = list(set(targets[1]))
        return targets

    def get_target(self, target_attack: List, card: str, player: int) -> Dict[int, List[str | int]]:
        try:
            return {
                "self": self.get_target_self,
                "player": self.get_target_player,
                "opponent": self.get_target_opponent,
                "player hand": self.get_target_player_hand,
                "player deck": self.get_target_player_deck,
                "player remaining": self.get_target_player_remaining,
                "opponent hand": self.get_target_opponent_hand,
                "opponent deck": self.get_target_opponent_deck,
                "opponent remaining": self.get_target_opponent_remaining,
                "both hand": self.get_target_both_hand,
                "both deck": self.get_target_both_deck,
                "both remaining": self.get_target_both_remaining,
            }[target_attack[0]](target_attack, card, player)
        except KeyError:
            raise TargetKeyError(f"Target {target_attack} inconnue")

    def get_target_self(self, target_attack: List, card: str, player: int) -> Dict[int, List[str]]:
        return {player: [card], 1 - player: []}

    def get_target_player(self, target_attack: List, card: str, player: int) -> Dict[int, List[int]]:
        return {player: [player], 1 - player: []}

    def get_target_opponent(self, target_attack: List, card: str, player: int) -> Dict[int, List[int]]:
        return {player: [1 - player], 1 - player: []}

    def get_target_player_hand(self, target_attack: List, card: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cards(target_attack, player, "hand")

    def get_target_player_deck(self, target_attack: List, card: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cards(target_attack, player, "order")

    def get_target_player_remaining(self, target_attack: List, card: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cards(target_attack, player, "remaining")

    def get_target_opponent_hand(self, target_attack: List, card: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cards(target_attack, 1 - player, "hand")

    def get_target_opponent_deck(self, target_attack: List, card: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cards(target_attack, 1 - player, "order")

    def get_target_opponent_remaining(self, target_attack: List, card: str, player: int) -> Dict[int, List[str]]:
        return self.get_target_cards(target_attack, 1 - player, "remaining")

    def get_target_both_hand(self, target_attack: List, card: str, player: int) -> Dict[int, List[str]]:
        dict0 = self.get_target_cards(target_attack, player, "hand")
        dict1 = self.get_target_cards(target_attack, 1 - player, "hand")
        dict0.update(dict1)
        return dict0

    def get_target_both_deck(self, target_attack: List, card: str, player: int) -> Dict[int, List[str]]:
        dict0 = self.get_target_cards(target_attack, player, "order")
        dict1 = self.get_target_cards(target_attack, 1 - player, "order")
        dict0.update(dict1)
        return dict0

    def get_target_both_remaining(self, target_attack: List, card: str, player: int) -> Dict[int, List[str]]:
        dict0 = self.get_target_cards(target_attack, player, "remaining")
        dict1 = self.get_target_cards(target_attack, 1 - player, "remaining")
        dict0.update(dict1)
        return dict0

    def get_target_cards(
        self,
        atk_target: List,
        player_targeted: int,
        location: Literal["hand", "order", "remaining"],
    ) -> Dict[int, List[str]]:
        # N'importe
        if len(atk_target) == 1:
            targets = {0: [], 1: []}
            targets[player_targeted] = self.decks[player_targeted].__getattribute__(location)
            return targets
        # Collection ou Album spécifique
        else:
            return {
                "name": self.get_target_cards_card,
                "collection": self.get_target_cards_deck,
                "album": self.get_target_cards_deck,
            }[atk_target[1]](atk_target, player_targeted, location)

    def get_target_cards_card(
        self,
        atk_target: List,
        player_targeted: int,
        location: Literal["hand", "order", "remaining"],
    ) -> Dict:
        targets = {0: [], 1: []}
        try:
            card_id_targeted = self.decks[player_targeted].name_to_id[atk_target[2]]
        except KeyError:
            return targets
        if card_id_targeted in self.decks[player_targeted].__getattribute__(location):
            targets[player_targeted].append(card_id_targeted)
            return targets
        return targets

    def get_target_cards_deck(
        self,
        atk_target: List,
        player_targeted: int,
        location: Literal["hand", "order", "remaining"],
    ) -> Dict:
        targets = {0: [], 1: []}
        for card_id in self.decks[player_targeted].__getattribute__(location):
            if self.decks[player_targeted].cards[card_id].__getattribute__(atk_target[1]) == atk_target[2]:
                targets[player_targeted].append(card_id)
        return targets

    """___Effect________________________________________________________________________________"""

    def apply_effects(
        self,
        atk_effect: List,
        atk_mult: List,
        atk_duree: List,
        targets: Dict[int, List],
        player: int,
    ) -> None:
        try:
            {
                "power": self.apply_effect_card,
                "burn": self.apply_effect_card,
                "cost": self.apply_effect_card,
                "lock": self.apply_effect_card_lock,
                "energy": self.apply_effect_energy,
                "power per turn": self.apply_effect_resource_per_turn,
                "energy per turn": self.apply_effect_resource_per_turn,
            }[atk_effect[0]](atk_effect, atk_mult, atk_duree, targets, player)
        except KeyError:
            raise EffectKeyError(f"Effect <{atk_effect[0]}> inconnu")

    def apply_effect_card(
        self,
        atk_effect: List,
        atk_mult: List,
        atk_duree: List,
        targets: Dict[int, List],
        player: int,
    ) -> None:
        index = self.get_index_from_duree(atk_duree)
        mult = 1 if atk_mult == [] else self.get_multiplicateur(atk_mult, player)
        for player in range(2):
            for card in targets[player]:
                self.decks[player].cards[card].buff[atk_effect[0]][index] += int(atk_effect[1]) * mult

    def apply_effect_card_lock(
        self,
        atk_effect: List,
        atk_mult: List,
        atk_duree: List,
        targets: Dict[int, List],
        player: int,
    ) -> None:
        index = self.get_index_from_duree(atk_duree)
        for player in range(2):
            for card in targets[player]:
                self.decks[player].cards[card].buff[atk_effect[0]][index] += 1

    def apply_effect_resource_per_turn(
        self,
        atk_effect: List,
        atk_mult: List,
        atk_duree: List,
        targets: Dict[int, List],
        player: int,
    ) -> None:
        data = atk_effect[0][:-9]
        player_targeted = targets[player][0]
        amount = int(atk_effect[1])
        index = self.get_index_from_duree(atk_duree)
        mult = 1 if atk_mult == [] else self.get_multiplicateur(atk_mult, player)
        self.resource_per_turn[data][player_targeted][index] += amount * mult

    def get_index_from_duree(self, duree: List) -> int:
        try:
            return {
                "turn": int(duree[1]) + 1,
                "round": int(duree[1]) * 3 - self.turn + 1,
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
        atk_effect: List,
        atk_mult: List,
        atk_duree: List,
        targets: Dict[int, List],
        player: int,
    ) -> None:
        self.energy[targets[player][0]] += int(atk_effect[1])

    """___Multiplicateur________________________________________________________________________"""

    def get_multiplicateur(self, attack_mult: List, player: int) -> int:
        return {
            "player hand": self.get_multiplicateur_hand,
            "player deck": self.get_multiplicateur_deck,
            "player played": self.get_multiplicateur_played,
            "player album": self.get_multiplicateur_album,
            "round completed": self.get_multiplicateur_round_completed,
            "both deck": self.get_multiplicateur_both_deck,
        }[attack_mult[0]](attack_mult, player)

    def get_multiplicateur_hand(self, attack_mult: List, player: int) -> int:
        multiplicateur = 0
        for card_id in self.decks[player].hand:
            if self.decks[player].cards[card_id].__getattribute__(attack_mult[1]) == attack_mult[2]:
                multiplicateur += 1
        return self.get_maxed_multiplicateur(multiplicateur, attack_mult, 3)

    def get_multiplicateur_deck(self, attack_mult: List, player: int) -> int:
        try:
            return self.get_maxed_multiplicateur(self.stats[player][attack_mult[1]][attack_mult[2]], attack_mult, 3)
        except KeyError:
            return 0

    def get_multiplicateur_played(self, attack_mult: List, player: int) -> int:
        return self.get_maxed_multiplicateur({
            "name": self.get_multiplicateur_played_card,
            "collection": self.get_multiplicateur_played_deck,
            "album": self.get_multiplicateur_played_deck,
        }[attack_mult[1]](attack_mult, player), attack_mult, 3)

    def get_multiplicateur_album(self, attack_mult: List, player: int) -> int:
        return len(self.stats[player]["album"])

    def get_multiplicateur_played_card(self, attack_mult: List, player: int) -> int:
        try:
            card_id = self.decks[player].name_to_id[attack_mult[2]]
        except KeyError:
            raise CarteAbsenteDuDeck()
        return self.decks[player].cards[card_id].played

    def get_multiplicateur_played_deck(self, attack_mult: List, player: int) -> int:
        multiplicateur = 0
        for card in self.decks[player].cards.values():
            if card.__getattribute__(attack_mult[1]) == attack_mult[2]:
                multiplicateur += card.played
        return multiplicateur

    def get_multiplicateur_round_completed(self, attack_mult: List, player: int) -> int:
        return self.round

    def get_multiplicateur_both_deck(self, atk_mult: List, player: int) -> int:
        mult_player0 = self.get_multiplicateur_played_deck(atk_mult, 0)
        mult_player1 = self.get_multiplicateur_played_deck(atk_mult, 1)
        return mult_player0 + mult_player1

    def get_maxed_multiplicateur(self, multiplicateur: int, attack_mult: List, index: int) -> int:
        try:
            return min(multiplicateur, int(attack_mult[index]))
        except IndexError:
            return multiplicateur

    """___Miscellaneous_________________________________________________________________________"""

    def count_turn(self) -> None:
        self.turn += 1
        if self.turn == self.turns:
            self.turn = 0
            self.round += 1
            self.check_end_game()

    @property
    def players_rounds(self) -> List[int]:
        players_rounds = [0, 0]
        for round in range(self.rounds):
            round_score_player0 = np.sum(self.score[round, :, 0])
            round_score_player1 = np.sum(self.score[round, :, 1])
            if round_score_player0 > round_score_player1:
                players_rounds[0] += 1
            elif round_score_player1 > round_score_player0:
                players_rounds[1] += 1
        return players_rounds

    def check_end_game(self) -> None:
        rounds_player0, rounds_player1 = self.players_rounds
        if self.rounds - self.round < rounds_player0 - rounds_player1:
            self.winner = 0
            self.end_game()
        elif self.rounds - self.round < rounds_player1 - rounds_player0:
            self.winner = 1
            self.end_game()
        elif self.round == self.rounds:
            self.winner = None
            self.end_game()

    def end_game(self) -> None:
        pass
