from src.models.Song import Song
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
    game_manager = GameManager()

    list_adder.add_player("A", [Song("song 1"), Song("song 2"), Song("song 4")])
    assert set(data_viewer.get_players_from_song(Song("song 1"))) == {"A"}
    assert set(data_viewer.get_players_from_song(Song("song 2"))) == {"A"}
    assert set(data_viewer.get_players_from_song(Song("song 3"))) == set()
    assert set(data_viewer.get_players_from_song(Song("song 4"))) == {"A"}
    assert set(data_viewer.get_players_from_song(Song("song 5"))) == set()
    assert set(data_viewer.get_players_from_song(Song("song 6"))) == set()
    list_adder.add_player("B", [Song("song 1"), Song("song 2"), Song("song 3"), Song("song 5")])
    assert set(data_viewer.get_players_from_song(Song("song 1"))) == {"A", "B"}
    assert set(data_viewer.get_players_from_song(Song("song 2"))) == {"A", "B"}
    assert set(data_viewer.get_players_from_song(Song("song 3"))) == {"B"}
    assert set(data_viewer.get_players_from_song(Song("song 4"))) == {"A"}
    assert set(data_viewer.get_players_from_song(Song("song 5"))) == {"B"}
    assert set(data_viewer.get_players_from_song(Song("song 6"))) == set()
    #indicating that C has a type in song 1, and so manually merge the typo 1' into 1
    list_adder.add_player("C", [Song("song 1'"), Song("song 3"), Song("song 6")])
    assert set(data_viewer.get_players_from_song(Song("song 1"))) == {"A", "B"}
    assert set(data_viewer.get_players_from_song(Song("song 1'"))) == {"C"}
    game_manager.merge_songs(Song("song 1"), Song("song 1'"))
    assert set(data_viewer.get_players_from_song(Song("song 1"))) == {"A", "B", "C"}
    assert set(data_viewer.get_players_from_song(Song("song 2"))) == {"A", "B"}
    assert set(data_viewer.get_players_from_song(Song("song 3"))) == {"B", "C"}
    assert set(data_viewer.get_players_from_song(Song("song 4"))) == {"A"}
    assert set(data_viewer.get_players_from_song(Song("song 5"))) == {"B"}
    assert set(data_viewer.get_players_from_song(Song("song 6"))) == {"C"}

    assert set(data_viewer.get_all_players()) == {"A", "B", "C"}
    assert set(song.song_title for song in data_viewer.get_songs()) == {"song 1", "song 2", "song 3", "song 4", "song 5", "song 6"}

    assert set(data_viewer.get_song_indices()) == {1,2,3,4,5,7}
    assert data_viewer.get_song_index(Song("song 1")) == 1
    assert data_viewer.get_song_index(Song("song 2")) == 2
    assert data_viewer.get_song_index(Song("song 3")) == 4
    assert data_viewer.get_song_index(Song("song 4")) == 3
    assert data_viewer.get_song_index(Song("song 5")) == 5
    assert data_viewer.get_song_index(Song("song 6")) == 7

def voting():
    voter = Voter()
    data_viewer = DataViewer()

    voter.add_votes_from_titles(["song 1", "song 2", "song 4"])
    assert data_viewer.get_votes(1) == 1
    assert data_viewer.get_votes(2) == 1
    assert data_viewer.get_votes(4) == 0
    assert data_viewer.get_votes(3) == 1
    assert data_viewer.get_votes(5) == 0
    assert data_viewer.get_votes(7) == 0
    voter.add_votes_from_titles(["song 1", "song 2", "song 3", "song 4"])
    assert data_viewer.get_votes_from_song(Song("song 1")) == 2
    assert data_viewer.get_votes_from_song(Song("song 2")) == 2
    assert data_viewer.get_votes_from_song(Song("song 3")) == 1
    assert data_viewer.get_votes_from_song(Song("song 4")) == 2
    assert data_viewer.get_votes_from_song(Song("song 5")) == 0
    assert data_viewer.get_votes_from_song(Song("song 6")) == 0
    voter.add_votes_from_titles(["song 1", "song 2", "song 3", "song 4", "song 6"])
    assert data_viewer.get_votes_from_song(Song("song 1")) == 3
    assert data_viewer.get_votes_from_song(Song("song 2")) == 3
    assert data_viewer.get_votes_from_song(Song("song 3")) == 2
    assert data_viewer.get_votes_from_song(Song("song 4")) == 3
    assert data_viewer.get_votes_from_song(Song("song 5")) == 0
    assert data_viewer.get_votes_from_song(Song("song 6")) == 1
    voter.add_votes_to_song(5, 2)
    assert data_viewer.get_votes_from_song(Song("song 1")) == 3
    assert data_viewer.get_votes_from_song(Song("song 2")) == 3
    assert data_viewer.get_votes_from_song(Song("song 3")) == 2
    assert data_viewer.get_votes_from_song(Song("song 4")) == 3
    assert data_viewer.get_votes_from_song(Song("song 5")) == 2
    assert data_viewer.get_votes_from_song(Song("song 6")) == 1

def scoring():
    scorer = Scorer()

    #this is also testing if the tally board can happen without initiating it
    assert scorer.get_tally_board() == [("A", 11/3), ("B", 19/6), ("C", pytest.approx(7/6))]

    assert scorer.song_scores[1]["score"] == 2/3
    assert scorer.song_scores[2]["score"] == 1
    assert scorer.song_scores[4]["score"] == 1/2
    assert scorer.song_scores[3]["score"] == 2
    assert scorer.song_scores[5]["score"] == 1
    assert scorer.song_scores[7]["score"] == 0

    assert "A" in scorer.player_score
    assert set(scorer.player_score["A"].songs.keys()) == {"song 1 - Unknown", "song 2 - Unknown", "song 4 - Unknown"}
    assert scorer.player_score["A"].songs["song 1 - Unknown"]["score"] == 2/3
    assert scorer.player_score["A"].songs["song 2 - Unknown"]["score"] == 1
    assert scorer.player_score["A"].songs["song 4 - Unknown"]["score"] == 2
    assert scorer.player_score["A"].total == 11/3

    assert "B" in scorer.player_score
    assert set(scorer.player_score["B"].songs.keys()) == {"song 1 - Unknown", "song 2 - Unknown", "song 3 - Unknown", "song 5 - Unknown"}
    assert scorer.player_score["B"].songs["song 1 - Unknown"]["score"] == 2/3
    assert scorer.player_score["B"].songs["song 2 - Unknown"]["score"] == 1
    assert scorer.player_score["B"].songs["song 3 - Unknown"]["score"] == 1/2
    assert scorer.player_score["B"].songs["song 5 - Unknown"]["score"] == 1
    assert scorer.player_score["B"].total == 19/6

    assert "C" in scorer.player_score
    assert set(scorer.player_score["C"].songs.keys()) == {"song 1 - Unknown", "song 3 - Unknown", "song 6 - Unknown"}
    assert scorer.player_score["C"].songs["song 1 - Unknown"]["score"] == 2/3
    assert scorer.player_score["C"].songs["song 3 - Unknown"]["score"] == 1/2
    assert scorer.player_score["C"].songs["song 6 - Unknown"]["score"] == 0
    assert scorer.player_score["C"].total == pytest.approx(7/6)
    
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