from src.DataUsers.DataUser import DataUser

class DataViewer(DataUser):
    def get_current_game(self):
        return self.data_store.get_current_game()
    
    def get_game_phase(self, game_index):
        return self.data_store.get_game_phase(game_index)
    
    def get_game_prompt(self, game_index: int):
        return self.data_store.get_game_prompt(game_index)

    def get_songs(self):
        return self.data_store.get_songs()
    
    def get_all_players(self):
        return self.data_store.get_all_players()
    
    def get_players(self, song: str):
        return self.data_store.get_players(song)
    
    def get_votes(self, song: str):
        return self.data_store.get_votes(song)