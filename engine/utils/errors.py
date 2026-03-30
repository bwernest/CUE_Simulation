"""___Classes___________________________________________________________________________________"""


class CUE_SimulationException(Exception):
    pass


class CarteAbsenteDuDeck(CUE_SimulationException):
    pass


class CarteCycleeNonEnMain(CUE_SimulationException):
    pass


class CarteIncorrecte(CUE_SimulationException):
    pass


class CarteInexistante(CUE_SimulationException):
    pass


class ComparaisonKeyError(CUE_SimulationException):
    pass


class ConditionKeyError(CUE_SimulationException):
    pass


class DeckIncorrect(CUE_SimulationException):
    pass


class DureeKeyError(CUE_SimulationException):
    pass


class EffectKeyError(CUE_SimulationException):
    pass


class FiltreKeyError(CUE_SimulationException):
    pass


class MultiplicateurKeyError(CUE_SimulationException):
    pass


class NombreIncorrectDeCartes(CUE_SimulationException):
    pass


class PlayIncorrect(CUE_SimulationException):
    pass


class SettingsNotAvailable(CUE_SimulationException):
    pass


class TargetKeyError(CUE_SimulationException):
    pass
