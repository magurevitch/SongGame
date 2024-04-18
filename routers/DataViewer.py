from fastapi import APIRouter
from src.DataUsers.DataViewer import DataViewer

data_viewer = DataViewer()
router = APIRouter(prefix="/viewer")

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