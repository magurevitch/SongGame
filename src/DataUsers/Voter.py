from src.Phases import Phase
from src.DataUsers.DataUser import DataUser
from src.utils import extract_song

class Voter(DataUser):
    restricted_phase = Phase.VOTE

    def add_votes_from_titles(self, songs: list[str]):
        self.add_votes([self.get_song_index(extract_song(song)) for song in songs])

    def add_votes(self, songs: list[int]):
        self.data_store.add_votes_from_list(songs)

    def add_votes_to_song(self, song: int, votes: int):
        self.data_store.add_votes_to_song(song, votes)