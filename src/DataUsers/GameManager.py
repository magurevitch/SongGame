from src.Phases import Phase
from src.DataUsers.DataUser import DataUser

class GameManager(DataUser):
    restricted_phase = Phase.ADMIN

    def reset_tables(self):
        self.data_store.reset_tables()

    def start_game(self, prompt: str):
        return self.data_store.start_new_game(prompt)
    
    def change_phase(self, index: int, phase: Phase):
        self.data_store.change_phase(index, phase)

    def advance_current_phase(self):
        index = self.data_store.get_current_game()
        phase = self.data_store.get_game_phase(index)
        print(phase)
        print(phase.next())
        self.change_phase(index, phase.next())

    def merge_songs(self, song1: str, song2: str):
        self.data_store.merge_songs(song1, song2)