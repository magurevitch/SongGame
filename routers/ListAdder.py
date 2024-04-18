from fastapi import APIRouter
from src.ListAdder import ListAdder

list_adder = ListAdder()
router = APIRouter(prefix="/list")

@router.post("/add")
def get_all_players(request):
    list_adder.add_player(request["player"], request["songs"])
    return {}

@router.post("/merge")
def get_songs(request):
    list_adder.merge_songs(request["source_song"], request["target_song"])
    return {}
