from fastapi import APIRouter
from src.DataUsers.DataViewer import DataViewer
from src.models.ApiModels import MergeSongs, StartGame
from src.Phases import Phase
from src.DataUsers.GameManager import GameManager

game_manager = GameManager()
data_viewer = DataViewer()
router = APIRouter(prefix="/admin")

@router.post("/phase/{phase}")
def change_game_phase(phase: str):
    game_index = game_manager.data_store.get_current_game()
    game_manager.change_phase(game_index, Phase[phase])
    return {}

@router.post("/merge")
def merge_songs(request: MergeSongs):
    game_manager.merge_songs(request.source_song, request.target_song)
    return {"songs": data_viewer.get_songs()}

@router.post("/rename")
def rename_song(request: MergeSongs):
    game_manager.rename_song(request.source_song, request.target_song)
    return {}

@router.post("/start")
def start_new_game(request: StartGame):
    return {"game_index": game_manager.start_game(request.prompt)}