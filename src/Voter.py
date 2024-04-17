from src.DataStore import DataStore

class Voter():
    def __init__(self, is_test=False):
        self.data_store = DataStore(is_test)

    def add_votes(self, songs: list[str]):
        self.data_store.add_votes_from_list(songs)

    def add_votes_to_song(self, song: str, votes: int):
        self.data_store.add_votes_to_song(song, votes)