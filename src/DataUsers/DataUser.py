from src.models.Song import Song
from src.DataStore import DataStore

class DataUser:
    data_store = DataStore()
    restricted_phase = None

    def is_allowed(self, index: int) -> bool:
        return True if self.restricted_phase is None else self.data_store.get_game_phase(index) == self.restricted_phase
    
    def get_song_index(self, song: Song) -> int:
        game_index = self.data_store.get_current_game()
        return self.data_store.get_song_index(game_index, song)