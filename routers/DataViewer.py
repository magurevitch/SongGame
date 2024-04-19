from fastapi import APIRouter
from src.DataUsers.DataViewer import DataViewer

data_viewer = DataViewer()
router = APIRouter(prefix="/viewer")

@router.get("/game")
def get_current_game():
    return {"game": data_viewer.get_current_game()}

@router.get("/game/{index}")
def get_current_game(index: int):
    return {"prompt": data_viewer.get_game_prompt(index)}

@router.get("/phase/{index}")
def get_game_phase(index: int):
    return {"phase": data_viewer.get_game_phase(index)}

@router.get("/players")
def get_all_players():
    return {"players": list(data_viewer.get_all_players())}

@router.get("/songs")
def get_songs():
    return {"songs": list(data_viewer.get_songs())}

@router.get("/players/{song}")
def get_players(song: str):
    return {"players": list(data_viewer.get_players(song))}

@router.get("/votes/{song}")
def get_votes(song: str):
    return {"votes": data_viewer.get_votes(song)}