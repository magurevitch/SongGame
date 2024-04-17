class Song:
    def __init__(self):
        self.players = []
        self.votes = 0

    def score(self):
        # current algorithm assumes that since everyone votes for themself, ignore theirs
        return (self.votes-1) / len(self.players)

class Result:
    def __init__(self):
        self.total = 0
        self.songs = {}

    def __repr__(self):
        return "total: {}, songs: {}".format(self.total, self.songs)

class SongBank:
    def __init__(self):
        self.songs = {}
        self.players = []
        self.score = None

    def add_player(self, player: str, songs: list[str]):
        if player in self.players:
            raise Exception()
        self.score = None
        self.players.append(player)
        for song in songs:
            if song not in self.songs:
                self.songs[song] = Song()
            self.songs[song].players.append(player)

    def add_votes(self, songs: list[str]):
        self.score = None
        for song in songs:
            if song not in self.songs:
                raise Exception()
            self.songs[song].votes += 1

    def get_score(self):
        if self.score:
            return self.score
        return self.makeScore()
    
    def get_songs(self):
        return self.songs.keys()
    
    def merge_songs(self, song1, song2):
        if song1 not in self.songs or song2 not in self.songs:
            raise KeyError()
        self.score = None
        self.songs[song1].players.extend(self.songs[song2].players)
        del self.songs[song2]
    
    def makeScore(self) -> dict[str, dict]:
        score = {player: Result() for player in self.players}
        for song, data in self.songs.items():
            for player in data.players:
                score[player].total += data.score()
                score[player].songs[song] = data.score()
        self.score = score
        return score
    
    def make_tally_board(self) -> list[tuple[str, float]]:
        return sorted([(player, result.total) for player, result in self.get_score().items()], key=lambda x: -x[1])
    
    def get_detailed_breakdown(self, player):
        if player not in self.players:
            raise KeyError()
        return self.get_score()[player]