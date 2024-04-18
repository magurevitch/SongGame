from fastapi import APIRouter
from src.Voter import Voter

voter = Voter()
router = APIRouter(prefix="/vote")

@router.post("/")
def add_votes(request):
    voter.add_votes(request["songs"])
    return {}

@router.post("/{song}")
def add_votes_to_song(song: str, request):
    voter.add_votes_to_song(song, request["votes"])
    return {}
