from src.DataUsers.GameManager import GameManager
from src.DataUsers.DataViewer import DataViewer
from src.DataUsers.ListAdder import ListAdder
from src.DataUsers.Voter import Voter
from src.DataUsers.Scorer import Scorer
import pytest

def new_game():
    game_manager = GameManager()
    data_viewer = DataViewer()

    assert data_viewer.get_current_game() == None

    game_manager.start_game("test")

    assert data_viewer.get_current_game() == 1
    assert data_viewer.get_game_prompt(1) == "test"

def adding_lists():
    list_adder = ListAdder()
    data_viewer = DataViewer()

    list_adder.add_player("A", ["1", "2", "4"])
    assert set(data_viewer.get_players("1")) == {"A"}
    assert set(data_viewer.get_players("2")) == {"A"}
    assert set(data_viewer.get_players("3")) == set()
    assert set(data_viewer.get_players("4")) == {"A"}
    assert set(data_viewer.get_players("5")) == set()
    assert set(data_viewer.get_players("6")) == set()
    list_adder.add_player("B", ["1", "2", "3", "5"])
    assert set(data_viewer.get_players("1")) == {"A", "B"}
    assert set(data_viewer.get_players("2")) == {"A", "B"}
    assert set(data_viewer.get_players("3")) == {"B"}
    assert set(data_viewer.get_players("4")) == {"A"}
    assert set(data_viewer.get_players("5")) == {"B"}
    assert set(data_viewer.get_players("6")) == set()
    #indicating that C has a type in song 1, and so manually merge the typo 1' into 1
    list_adder.add_player("C", ["1'", "3", "6"])
    assert set(data_viewer.get_players("1")) == {"A", "B"}
    assert set(data_viewer.get_players("1'")) == {"C"}
    list_adder.merge_songs("1", "1'")
    assert set(data_viewer.get_players("1")) == {"A", "B", "C"}
    assert set(data_viewer.get_players("2")) == {"A", "B"}
    assert set(data_viewer.get_players("3")) == {"B", "C"}
    assert set(data_viewer.get_players("4")) == {"A"}
    assert set(data_viewer.get_players("5")) == {"B"}
    assert set(data_viewer.get_players("6")) == {"C"}

    assert set(data_viewer.get_all_players()) == {"A", "B", "C"}
    assert set(data_viewer.get_songs()) == {"1", "2", "3", "4", "5", "6"}

def voting():
    voter = Voter()
    data_viewer = DataViewer()

    voter.add_votes(["1", "2", "4"])
    assert data_viewer.get_votes("1") == 1
    assert data_viewer.get_votes("2") == 1
    assert data_viewer.get_votes("3") == 0
    assert data_viewer.get_votes("4") == 1
    assert data_viewer.get_votes("5") == 0
    assert data_viewer.get_votes("6") == 0
    voter.add_votes(["1", "2", "3", "4", "5"])
    assert data_viewer.get_votes("1") == 2
    assert data_viewer.get_votes("2") == 2
    assert data_viewer.get_votes("3") == 1
    assert data_viewer.get_votes("4") == 2
    assert data_viewer.get_votes("5") == 1
    assert data_viewer.get_votes("6") == 0
    voter.add_votes(["1", "2", "3", "4", "5", "6"])
    assert data_viewer.get_votes("1") == 3
    assert data_viewer.get_votes("2") == 3
    assert data_viewer.get_votes("3") == 2
    assert data_viewer.get_votes("4") == 3
    assert data_viewer.get_votes("5") == 2
    assert data_viewer.get_votes("6") == 1

def scoring():
    scorer = Scorer()

    assert scorer.song_scores["1"] == 2/3
    assert scorer.song_scores["2"] == 1
    assert scorer.song_scores["3"] == 1/2
    assert scorer.song_scores["4"] == 2
    assert scorer.song_scores["5"] == 1
    assert scorer.song_scores["6"] == 0

    assert "A" in scorer.player_score
    assert set(scorer.player_score["A"].songs.keys()) == {"1", "2", "4"}
    assert scorer.player_score["A"].songs["1"] == 2/3
    assert scorer.player_score["A"].songs["2"] == 1
    assert scorer.player_score["A"].songs["4"] == 2
    assert scorer.player_score["A"].total == 11/3

    assert "B" in scorer.player_score
    assert set(scorer.player_score["B"].songs.keys()) == {"1", "2", "3", "5"}
    assert scorer.player_score["B"].songs["1"] == 2/3
    assert scorer.player_score["B"].songs["2"] == 1
    assert scorer.player_score["B"].songs["3"] == 1/2
    assert scorer.player_score["B"].songs["5"] == 1
    assert scorer.player_score["B"].total == 19/6

    assert "C" in scorer.player_score
    assert set(scorer.player_score["C"].songs.keys()) == {"1", "3", "6"}
    assert scorer.player_score["C"].songs["1"] == 2/3
    assert scorer.player_score["C"].songs["3"] == 1/2
    assert scorer.player_score["C"].songs["6"] == 0
    assert scorer.player_score["C"].total == pytest.approx(7/6)
    
    assert scorer.get_tally_board() == [("A", 11/3), ("B", 19/6), ("C", pytest.approx(7/6))]

def test_song_game_functions():
    '''
    songs:
    song 1: on 3 lists, 3 votes
    song 2: on 2 lists, 3 votes
    song 3: on 2 lists, 2 votes
    song 4: on 1 list,  3 votes
    song 5: on 1 list,  2 votes
    song 6: on 1 list,  1 vote

    players:
    player A: list is 1, 2, 4
    player B: list is 1, 2, 3, 5
    player C: list is 1, 3, 6
    '''

    GameManager().reset_tables()
    assert DataViewer().get_current_game() is None

    new_game()
    adding_lists()
    voting()
    scoring()

    GameManager().reset_tables()
    assert DataViewer().get_current_game() is None