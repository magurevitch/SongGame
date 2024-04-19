from src.DataUsers.DataUser import DataUser
from src.Phases import Phase

class Result:
    def __init__(self):
        self.total = 0
        self.songs = {}

    def __repr__(self):
        return "total: {}, songs: {}".format(self.total, self.songs)

class Scorer(DataUser):
    restricted_phase = Phase.SCORE
    
    def make_scores(self) -> dict[str, dict]:
        def make_song_score(song):
            votes = self.data_store.get_votes(song)
            players = list(self.data_store.get_players(song))
            # current algorithm assumes that since everyone votes for themself, ignore theirs
            return (votes-1) / len(players)
        self.song_scores = {song: make_song_score(song) for song in self.data_store.get_songs()}
        
        self.player_score = {player: Result() for player in self.data_store.get_all_players()}
        for song, player in self.data_store.get_player_lists():
            self.player_score[player].total += self.song_scores[song]
            self.player_score[player].songs[song] = self.song_scores[song]
    
    def get_tally_board(self) -> list[tuple[str, float]]:
        return sorted([(player, result.total) for player, result in self.player_score.items()], key=lambda x: -x[1])
    
    def get_detailed_breakdown(self, player: str) -> Result:
        return self.player_score[player]