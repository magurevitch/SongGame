from src.models.Song import Song
from src.Phases import Phase
from src.DataUsers.DataUser import DataUser

class ListAdder(DataUser):
    restricted_phase = Phase.ADD_LIST

    def add_player(self, player: str, songs: list[Song]):
        self.data_store.add_player_list(player, songs)