import asyncio
from src.DataUsers.DataUser import DataUser
from src.Phases import Phase
from src.utils import lock

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
    
    @lock
    async def make_scores(self):
        def make_song_score(song):
            votes = self.data_store.get_votes(song)
            players = len(list(self.data_store.get_players(song)))
            return {"score": calculate_score(votes, players), "votes": votes, "players": players}
        
        self.song_scores = {song: make_song_score(song) for song in self.data_store.get_all_song_indices()}
        
        self.player_score = {player: Result() for player in self.data_store.get_all_players()}
        for song, player in self.data_store.get_player_lists():
            self.player_score[player].total += self.song_scores[song]["score"]
            song_object = self.data_store.get_song_details(song)
            self.player_score[player].songs[str(song_object)] = self.song_scores[song]

    def get_player_score(self):
        if hasattr(self, 'player_score'):
            return self.player_score
        asyncio.run(self.make_scores())
        return self.player_score

    def get_tally_board(self) -> list[tuple[str, float]]:
        return sorted([(player, result.total) for player, result in self.get_player_score().items()], key=lambda x: -x[1])
    
    def get_detailed_breakdown(self, player: str):
        return self.get_player_score()[player]