from src.DataUser import DataUser

class DataViewer(DataUser):
    def get_songs(self):
        return self.data_store.get_songs()
    
    def get_all_players(self):
        return self.data_store.get_all_players()
    
    def get_players(self, song: str):
        return self.data_store.get_players(song)
    
    def get_votes(self, song: str):
        return self.data_store.get_votes(song)