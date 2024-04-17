from src.DataStore import DataStore

class Result:
    def __init__(self):
        self.total = 0
        self.songs = {}

    def __repr__(self):
        return "total: {}, songs: {}".format(self.total, self.songs)

class SongBank:
    def __init__(self, is_test=False):
        self.song_scores = None
        self.player_score = None
        self.data_store = DataStore(is_test)

    def add_player(self, player: str, songs: list[str]):
        self.player_score = None
        self.data_store.add_player_list(player, songs)

    def add_votes(self, songs: list[str]):
        self.player_score = None
        self.data_store.add_votes_from_list(songs)

    def get_score(self):
        if not self.player_score:
            self.make_scores()
        return self.player_score

    def merge_songs(self, song1, song2):
        self.data_store.merge_songs(song1, song2)
    
    def make_scores(self) -> dict[str, dict]:
        def make_song_score(song):
            votes = self.data_store.get_votes(song)
            players = list(self.data_store.get_players(song))
            # current algorithm assumes that since everyone votes for themself, ignore theirs
            return (votes-1) / len(players)
        self.song_scores = {song: make_song_score(song) for song in self.data_store.get_songs()}
        
        score = {player: Result() for player in self.data_store.get_all_players()}
        for song, player in self.data_store.get_player_lists():
            score[player].total += self.song_scores[song]
            score[player].songs[song] = self.song_scores[song]
        self.player_score = score
    
    def make_tally_board(self) -> list[tuple[str, float]]:
        return sorted([(player, result.total) for player, result in self.get_score().items()], key=lambda x: -x[1])
    
    def get_detailed_breakdown(self, player):
        return self.get_score()[player]