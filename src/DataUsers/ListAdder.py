from src.Phases import Phase
from src.DataUsers.DataUser import DataUser

class ListAdder(DataUser):
    restricted_phase = Phase.ADD_LIST

    def add_player(self, player: str, songs: list[str]):
        self.data_store.add_player_list(player, songs)

    def merge_songs(self, song1: str, song2: str):
        self.data_store.merge_songs(song1, song2)