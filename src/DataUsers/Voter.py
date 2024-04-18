from src.DataUsers.DataUser import DataUser

class Voter(DataUser):
    def add_votes(self, songs: list[str]):
        self.data_store.add_votes_from_list(songs)

    def add_votes_to_song(self, song: str, votes: int):
        self.data_store.add_votes_to_song(song, votes)