"""___Classes___________________________________________________________________________________"""


class CUE_SimulationException(Exception):
    pass


class CarteIncorrecte(CUE_SimulationException):
    pass


class DeckIncorrect(CUE_SimulationException):
    pass


class NombreIncorrectDeCartes(CUE_SimulationException):
    pass


class PlayIncorrect(CUE_SimulationException):
    pass


class SettingsNotAvailable(CUE_SimulationException):
    pass
