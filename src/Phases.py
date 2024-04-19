from enum import Enum

class Phase(Enum):
    ADD_LIST = 0
    VOTE = 1
    SCORE = 2

    def next(self):
        value = self.value + 1
        return Phase(value) if value < len(Phase) else self