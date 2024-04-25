from fastapi import APIRouter
from src.DataUsers.Scorer import Scorer

scorer = Scorer()
router = APIRouter(prefix="/score")

@router.post("/")
def score():
    scorer.make_scores()
    return {}

@router.get("/tally")
def get_tally_board():
    tally_board = [{"player": player, "score": score} for player, score in scorer.get_tally_board()]
    return {"tally_board": tally_board}

@router.get("/player/{player}")
def get_detailed_breakdown(player: str):
    return {"breakdown": scorer.get_detailed_breakdown(player).__dict__}