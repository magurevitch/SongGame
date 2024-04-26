from src.DataUsers.DataUser import DataUser
from src.Phases import Phase

class Result:
    def __init__(self):
        self.total = 0
        self.songs = {}

    def __repr__(self):
        return "total: {}, songs: {}".format(self.total, self.songs)
    
def calculate_score(votes: int, players: int):
    # current algorithm assumes that since everyone votes for themself, ignore theirs
    return (votes-1) / players

class Scorer(DataUser):
    restricted_phase = Phase.SCORE

    def __init__(self) -> None:
        super().__init__()
        if self.data_store.get_current_game() is not None:
            self.make_scores()
    
    def make_scores(self):
        def make_song_score(song):
            votes = self.data_store.get_votes(song)
            players = len(list(self.data_store.get_players(song)))
            return {"score": calculate_score(votes, players), "votes": votes, "players": players}
        self.song_scores = {song: make_song_score(song) for song in self.data_store.get_songs()}
        
        self.player_score = {player: Result() for player in self.data_store.get_all_players()}
        for song, player in self.data_store.get_player_lists():
            self.player_score[player].total += self.song_scores[song]["score"]
            self.player_score[player].songs[song] = self.song_scores[song]

    def get_tally_board(self) -> list[tuple[str, float]]:
        return sorted([(player, result.total) for player, result in self.player_score.items()], key=lambda x: -x[1])
    
    def get_detailed_breakdown(self, player: str):
        return self.player_score[player]