from src.DataStore import DataStore

class Result:
    def __init__(self):
        self.total = 0
        self.songs = {}

    def __repr__(self):
        return "total: {}, songs: {}".format(self.total, self.songs)

class Scorer:
    def __init__(self, is_test=False):
        self.make_scores(is_test)
    
    def make_scores(self, is_test) -> dict[str, dict]:
        data_store = DataStore(is_test)
        def make_song_score(song):
            votes = data_store.get_votes(song)
            players = list(data_store.get_players(song))
            # current algorithm assumes that since everyone votes for themself, ignore theirs
            return (votes-1) / len(players)
        self.song_scores = {song: make_song_score(song) for song in data_store.get_songs()}
        
        self.player_score = {player: Result() for player in data_store.get_all_players()}
        for song, player in data_store.get_player_lists():
            self.player_score[player].total += self.song_scores[song]
            self.player_score[player].songs[song] = self.song_scores[song]
    
    def make_tally_board(self) -> list[tuple[str, float]]:
        return sorted([(player, result.total) for player, result in self.player_score.items()], key=lambda x: -x[1])
    
    def get_detailed_breakdown(self, player):
        return self.player_score[player]