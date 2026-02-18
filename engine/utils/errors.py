"""___Classes___________________________________________________________________________________"""


class CUE_SimulationException(Exception):
    pass


class DeckIncorrect(CUE_SimulationException):
    pass

class CardIncorrect(CUE_SimulationException):
    pass

class PlayIncorrect(CUE_SimulationException):
    pass

class SettingsNotAvailable(CUE_SimulationException):
    pass
