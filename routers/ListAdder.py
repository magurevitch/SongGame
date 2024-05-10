from fastapi import APIRouter
from src.models.ApiModels import PlayerList
from src.DataUsers.ListAdder import ListAdder
from src.utils import extract_song

list_adder = ListAdder()
router = APIRouter(prefix="/list")

@router.post("/add")
def add_player_list(request: PlayerList):
    list_adder.add_player(request.player, request.songs)
    return {}
