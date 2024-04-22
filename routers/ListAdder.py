from fastapi import APIRouter
from src.ApiModels import MergeSongs, PlayerList
from src.DataUsers.ListAdder import ListAdder

list_adder = ListAdder()
router = APIRouter(prefix="/list")

@router.post("/add")
def add_player_list(request: PlayerList):
    list_adder.add_player(request.player, request.songs)
    return {}

@router.post("/merge")
def get_songs(request: MergeSongs):
    list_adder.merge_songs(request.source_song, request.target_song)
    return {}
