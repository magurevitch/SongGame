from src.models.Song import Song
from src.DataUsers.DataUser import DataUser

class DataViewer(DataUser):
    def get_current_game(self):
        return self.data_store.get_current_game()
    
    def get_game_phase(self, game_index: int):
        return self.data_store.get_game_phase(game_index)
    
    def get_game_prompt(self, game_index: int):
        return self.data_store.get_game_prompt(game_index)

    def get_songs(self) -> list[Song]:
        song_indices = self.get_song_indices()
        return [self.data_store.get_song_details(index) for index in song_indices]
    
    def get_song_indices(self) -> list[int]:
        return self.data_store.get_all_song_indices()
    
    def get_all_players(self) -> list[str]:
        return self.data_store.get_all_players()
    
    def get_players_from_song(self, song: Song):
        song_index = self.get_song_index(song)
        if song_index is None:
            return []
        return self.get_players(song_index)
    
    def get_players(self, song_index: int):
        return self.data_store.get_players(song_index)

    def get_votes_from_song(self, song: Song):
        song_index = self.get_song_index(song)
        return self.get_votes(song_index)

    def get_votes(self, song_index: int):
        return self.data_store.get_votes(song_index)