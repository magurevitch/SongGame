from pydantic import BaseModel

class PlayerList(BaseModel):
    player: str
    songs: list[str]

class MergeSongs(BaseModel):
    source_song: str
    target_song: str

class MassVote(BaseModel):
    votes: int

class AddVotes(BaseModel):
    songs: list[str]