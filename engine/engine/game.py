"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .deck import Deck
from ..utils import *

# Python
import numpy as np
import numpy.typing as npt
from typing import Dict, List, Literal, Tuple

"""___Classes___________________________________________________________________________________"""


class Game(Deck):

    decks: List[Deck]

    score: npt.NDArray
    turn: int
    round: int
    winner: int | None

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
        self.power_per_turn = [0, 0]
        self.power_per_turn_buff = [[], []]
        self.energy = np.array([start_energy, start_energy])
        self.energy_per_turn = np.array([energy_per_turn, energy_per_turn])
        self.energy_per_turn_buff = [[], []]
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
        self.pre_play()

    def pre_play(self) -> None:
        self.trigger_attacks("draw")
        self.trigger_attacks("start")

    def play(self, play0: List[str | None], play1: List[str | None]) -> None:
        if not len(play0) == self.play_len or not len(play1) == self.play_len:
            raise PlayIncorrect("Nombre de cartes jouées incorrect")
        plays = [play0, play1]
        for player in range(2):
            for k in range(self.play_len):
                if plays[player][k] is None:
                    continue
                self.trigger_attack("play", plays[player][k], player)
                card = self.decks[player].cards[plays[player][k]]
                turn_score = 0
                turn_score += max(0, card.base_power - np.sum(card.buff["burn"]))
                turn_score += np.sum(card.buff["power"])
                self.score[self.round, self.turn,
                           player] += max(0, turn_score) + self.power_per_turn[player]
                self.energy[player] -= max(0, card.base_energy - np.sum(card.buff["energy"]))

        self.post_play(plays)

    def post_play(self, plays) -> None:
        for player in range(2):
            for k in range(self.play_len):
                if plays[player][k] is None:
                    continue
                self.trigger_attack("return", plays[player][k], player)
        self.energy += self.energy_per_turn
        self.energy = np.clip(self.energy, self.min_energy, self.max_energy)
        self.count_turn()

    """___Attack________________________________________________________________________________"""

    def trigger_attacks(self, trigger: Literal["draw", "start"]) -> None:
        for player in range(2):
            for card in self.decks[player].hand:
                for attack in self.decks[player].cards[card].attacks[trigger]:
                    if self.check_conditions(attack["condition"], attack["acondition"], player):
                        self.execute_attack(attack, card, player)

    def trigger_attack(self, trigger: Literal["play", "return"], card: str, player: int) -> None:
        for attack in self.decks[player].cards[card].attacks[trigger]:
            if self.check_conditions(attack["condition"], attack["acondition"], player):
                self.execute_attack(attack, card, player)

    def execute_attack(self, attack: Dict, card: str, player: int) -> None:
        targets = self.get_targets(attack["cible"], card, player)
        self.apply_effects(attack["effet"], attack["duree"], targets, player)

    """___Condition_____________________________________________________________________________"""

    def check_conditions(self, conditions: List, aconditions: List, player: int) -> bool:
        for line in conditions:
            if not self.check_condition(line, player):
                return False
        for line in aconditions:
            if self.check_condition(line, player):
                return False
        return True

    def check_condition(self, line: List, player: int) -> bool:
        try:
            return {
                "player deck": self.check_condition_pd,
                "turn score": self.check_condition_turn_score,
                "round score": self.check_condition_round_score,
            }[line[0]](line, player)
        except KeyError:
            raise KeyError(f"Condition {line[0]} inconnue")

    def check_condition_pd(self, line: List, player: int) -> bool:
        amount_deck = self.get_amount(player, line[1], line[2])
        amount_target = int(line[4])
        return self.check_condition_amount(line[3], amount_deck, amount_target)

    def check_condition_turn_score(self, line: List, player: int) -> bool:
        amount_turn_score = self.score[self.round, self.turn,
                                       player] - self.score[self.round, self.turn, 1 - player]
        amount_target = int(line[2])
        return self.check_condition_amount(line[1], amount_turn_score, amount_target)

    def check_condition_round_score(self, line: List, player: int) -> bool:
        amount_round_score = np.sum(
            self.score[self.round, :, player]) - np.sum(self.score[self.round, :, 1 - player])
        amount_target = int(line[2])
        return self.check_condition_amount(line[1], amount_round_score, amount_target)

    def check_condition_amount(self, comparaison: str, amount_player: int, amount_target: int) -> bool:
        try:
            return {
                "<": self.check_condition_amount_lt,
                ">": self.check_condition_amount_gt,
                "=": self.check_condition_amount_eq,
            }[comparaison](amount_player, amount_target)
        except KeyError:
            raise KeyError(f"Comparaison {comparaison} inconnue")

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

    def get_targets(self, target_attacks: List, card: str, player: int) -> Dict[int, List]:
        """
        Attention si la cible est un joueur
        """
        targets = {0: [], 1: []}
        for target_attack in target_attacks:
            target = self.get_target(target_attack, card, player)
            for player in range(2):
                if player in target:
                    targets[player] += target[player]
        targets[0] = list(set(targets[0]))
        targets[1] = list(set(targets[1]))
        return targets

    def get_target(self, target_attack: List, card: str, player: int) -> List:
        try:
            return {
                "self": self.get_target_self,
                "player": self.get_target_player,
                "opponent": self.get_target_opponent,
            }[target_attack](target_attack, card, player)
        except KeyError:
            raise KeyError(f"Target {target_attack} inconnue")

    def get_target_self(self, target_attack: List, card: str, player: int) -> List:
        return {player: [card]}

    def get_target_player(self, target_attack: List, card: str, player: int) -> List:
        return {player: [1]}

    def get_target_opponent(self, target_attack: List, card: str, player: int) -> List:
        return {1 - player: [1]}

    """___Effect________________________________________________________________________________"""

    def apply_effects(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        try:
            {
                "power": self.apply_effect_card,
                "burn": self.apply_effect_card,
                "energy": self.apply_effect_energy,
                "power_per_turn": self.apply_effect_player_per_turn,
                "energy_per_turn": self.apply_effect_player_per_turn,
            }[effect[0]](effect, duree, targets, player)
        except KeyError:
            raise KeyError(f"Effect {effect[0]} inconnu")

    def apply_effect_card(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        try:
            {
                "turn": self.apply_effect_card_turn,
                "round": self.apply_effect_card_round,
                "until_played": self.apply_effect_card_until_played,
                "permanently": self.apply_effect_card_permanently,
            }[duree[0]](effect, duree, targets, player)
        except KeyError:
            raise KeyError(f"Durée {duree[0]} inconnue")

    def apply_effect_player_per_turn(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        try:
            {
                "turn": self.apply_effect_player_per_turn_turn,
                "round": self.apply_effect_player_per_turn_round,
                "until_played": self.apply_effect_player_per_turn_until_played,
                "permanently": self.apply_effect_player_per_turn_permanently,
            }[duree[0]](effect, duree, targets)
        except KeyError:
            raise KeyError(f"Durée {duree[0]} inconnue")

    def apply_effect_player_per_turn_turn(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        pass

    def apply_effect_player_per_turn_round(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        pass

    def apply_effect_player_per_turn_until_played(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        pass

    def apply_effect_player_per_turn_permanently(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        pass

    def apply_effect_energy(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        self.energy[0] += int(effect[1]) * (targets[0] == [1])
        self.energy[1] += int(effect[1]) * (targets[1] == [1])

    def apply_effect_card_turn(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        for player in range(2):
            for card in targets[player]:
                self.decks[player].cards[card].buff[effect[0]][int(duree[1]) + 1] += int(effect[1])

    def apply_effect_card_round(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        for player in range(2):
            for card in targets[player]:
                self.decks[player].cards[card].buff[effect[0]][int(
                    duree[1]) * 3 - self.turn + 1] += int(effect[1])

    def apply_effect_card_until_played(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        for player in range(2):
            for card in targets[player]:
                self.decks[player].cards[card].buff[effect[0]][1] += int(effect[1])

    def apply_effect_card_permanently(self, effect: List, duree: List, targets: Dict[int, List], player: int) -> None:
        for player in range(2):
            for card in targets[player]:
                self.decks[player].cards[card].buff[effect[0]][0] += int(effect[1])

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
