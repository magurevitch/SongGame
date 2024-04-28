from pydantic import BaseModel

class MergeSongs(BaseModel):
    source_song: str
    target_song: str

class StartGame(BaseModel):
    prompt: str

class PlayerList(BaseModel):
    player: str
    songs: list[str]

class MassVote(BaseModel):
    votes: int

class AddVotes(BaseModel):
    songs: list[str]