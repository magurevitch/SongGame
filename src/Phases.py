from enum import Enum

class Phase(Enum):
    ADMIN = 0
    ADD_LIST = 1
    VOTE = 2
    SCORE = 3

    def next(self):
        value = self.value + 1
        return Phase(value) if value < len(Phase) else self