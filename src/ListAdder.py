from src.DataStore import DataStore

class ListAdder():
    def __init__(self, is_test=False):
        self.data_store = DataStore(is_test)

    def add_player(self, player: str, songs: list[str]):
        self.data_store.add_player_list(player, songs)

    def merge_songs(self, song1, song2):
        self.data_store.merge_songs(song1, song2)