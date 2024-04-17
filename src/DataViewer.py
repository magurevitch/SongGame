from src.DataStore import DataStore

class DataViewer():
    def __init__(self, is_test=False):
        self.data_store = DataStore(is_test)

    def get_songs(self):
        return self.data_store.get_songs()
    
    def get_all_players(self):
        return self.data_store.get_all_players()
    
    def get_players(self, song: str):
        return self.data_store.get_players(song)
    
    def get_votes(self, song: str):
        return self.data_store.get_votes(song)