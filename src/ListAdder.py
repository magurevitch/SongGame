from src.DataUser import DataUser

class ListAdder(DataUser):
    def add_player(self, player: str, songs: list[str]):
        self.data_store.add_player_list(player, songs)

    def merge_songs(self, song1, song2):
        self.data_store.merge_songs(song1, song2)