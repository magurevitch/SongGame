from pydantic import BaseModel

class Song(BaseModel):
    song_title: str
    artist: str

class MergeSongs(BaseModel):
    source_song: Song
    target_song: Song

class StartGame(BaseModel):
    prompt: str

class PlayerList(BaseModel):
    player: str
    songs: list[Song]

class MassVote(BaseModel):
    votes: int

class AddVotes(BaseModel):
    songs: list[Song]