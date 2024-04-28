from fastapi import APIRouter
from src.models.ApiModels import AddVotes, MassVote
from src.DataUsers.Voter import Voter
from src.utils import extract_song

voter = Voter()
router = APIRouter(prefix="/vote")

@router.post("/")
def add_votes(request: AddVotes):
    voter.add_votes([voter.get_song_index(extract_song(song)) for song in request.songs])
    return {}

@router.post("/{song}")
def add_votes_to_song(song: str, request: MassVote):
    voter.add_votes_to_song(song, request.votes)
    return {}
