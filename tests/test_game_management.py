from src.models.Song import Song
from src.Phases import Phase
from src.DataUsers.GameManager import GameManager
from src.DataUsers.DataViewer import DataViewer
from src.DataUsers.ListAdder import ListAdder
from src.DataUsers.Voter import Voter
from src.DataUsers.Scorer import Scorer

def test_new_game():
    game_manager = GameManager()
    data_viewer = DataViewer()
    list_adder = ListAdder()

    game_manager.reset_tables()

    assert data_viewer.get_current_game() is None

    game_manager.start_game("first")

    assert data_viewer.get_current_game() == 1
    assert data_viewer.get_game_prompt(1) == "first"

    assert set(data_viewer.get_all_players()) == set()
    assert set(data_viewer.get_songs()) == set()

    list_adder.add_player("A", [Song("1", "1"), Song("2")])
    list_adder.add_player("B", [Song("1", "1"), Song("2")])

    assert set(data_viewer.get_all_players()) == {"A", "B"}
    assert set(data_viewer.get_song_indices()) == {1, 2}
    assert set(str(song) for song in data_viewer.get_songs()) == {"1 - 1", "2 - Unknown"}
    assert set(data_viewer.get_players(1)) == {"A", "B"}
    assert set(data_viewer.get_players(2)) == {"A", "B"}

    game_manager.start_game("second")

    assert data_viewer.get_current_game() == 2
    assert data_viewer.get_game_prompt(2) == "second"

    list_adder.add_player("A", [Song("1", "1"), Song("3")])
    list_adder.add_player("C", [Song("1", "1"), Song("3")])

    assert set(data_viewer.get_all_players()) == {"A", "C"}
    assert set(data_viewer.get_song_indices()) == {3, 4}
    assert set(str(song) for song in data_viewer.get_songs()) == {"1 - 1", "3 - Unknown"}
    assert set(data_viewer.get_players(3)) == {"A", "C"}
    assert set(data_viewer.get_players(4)) == {"A", "C"}

    game_manager.reset_tables()

    assert data_viewer.get_current_game() is None

def test_phase_manager():
    game_manager = GameManager()
    data_viewer = DataViewer()
    list_adder = ListAdder()
    voter = Voter()
    scorer = Scorer()

    game_manager.reset_tables()

    assert data_viewer.get_current_game() is None

    game_manager.start_game("first")

    assert data_viewer.get_current_game() == 1
    assert data_viewer.get_game_phase(1) == Phase.ADD_LIST

    assert data_viewer.is_allowed(1)
    assert not game_manager.is_allowed(1)
    assert list_adder.is_allowed(1)
    assert not voter.is_allowed(1)
    assert not scorer.is_allowed(1)

    phase = game_manager.advance_current_phase()
    assert phase == Phase.VOTE

    assert data_viewer.get_current_game() == 1
    assert data_viewer.get_game_phase(1) == Phase.VOTE

    assert data_viewer.is_allowed(1)
    assert not game_manager.is_allowed(1)
    assert not list_adder.is_allowed(1)
    assert voter.is_allowed(1)
    assert not scorer.is_allowed(1)

    game_manager.start_game("second")
    
    assert data_viewer.get_current_game() == 2
    assert data_viewer.get_game_phase(1) == Phase.VOTE
    assert data_viewer.get_game_phase(2) == Phase.ADD_LIST

    assert data_viewer.is_allowed(1)
    assert not game_manager.is_allowed(1)
    assert not list_adder.is_allowed(1)
    assert voter.is_allowed(1)
    assert not scorer.is_allowed(1)

    assert list_adder.is_allowed(2)
    assert not voter.is_allowed(2)
    assert not scorer.is_allowed(2)

    game_manager.advance_current_phase()

    assert data_viewer.get_current_game() == 2
    assert data_viewer.get_game_phase(1) == Phase.VOTE
    assert data_viewer.get_game_phase(2) == Phase.VOTE

    assert data_viewer.is_allowed(1)
    assert not game_manager.is_allowed(1)
    assert not list_adder.is_allowed(2)
    assert voter.is_allowed(2)
    assert not scorer.is_allowed(2)

    game_manager.advance_current_phase()

    assert data_viewer.get_current_game() == 2
    assert data_viewer.get_game_phase(1) == Phase.VOTE
    assert data_viewer.get_game_phase(2) == Phase.SCORE

    assert data_viewer.is_allowed(1)
    assert not game_manager.is_allowed(1)
    assert not list_adder.is_allowed(2)
    assert not voter.is_allowed(2)
    assert scorer.is_allowed(2)

    game_manager.advance_current_phase()

    assert data_viewer.get_current_game() == 2
    assert data_viewer.get_game_phase(1) == Phase.VOTE
    assert data_viewer.get_game_phase(2) == Phase.SCORE

    assert data_viewer.is_allowed(1)
    assert not game_manager.is_allowed(1)
    assert not list_adder.is_allowed(2)
    assert not voter.is_allowed(2)
    assert scorer.is_allowed(2)

    game_manager.reset_tables()

    assert data_viewer.get_current_game() is None

def test_merge():
    game_manager = GameManager()
    data_viewer = DataViewer()
    list_adder = ListAdder()

    game_manager.reset_tables()
    assert data_viewer.get_current_game() is None
    game_manager.start_game("merge")

    list_adder.add_player("A", [Song("First"), Song("Second"), Song("Third")])
    list_adder.add_player("B", [Song("Fourth")])

    assert data_viewer.data_store.get_player_lists() == [(1, "A"), (2, "A"), (3, "A"), (4, "B")]

    game_manager.merge_songs(Song("Second"), Song("Third"))
    assert list(data_viewer.get_players_from_song(Song("Second"))) == ["A"]
    assert list(data_viewer.get_players_from_song(Song("Third"))) == []
    assert data_viewer.data_store.get_player_lists() == [(1, "A"), (2, "A"), (4, "B")]

    game_manager.merge_songs(Song("First"), Song("Fourth"))

    assert list(data_viewer.get_players_from_song(Song("First"))) == ["A", "B"]
    assert list(data_viewer.get_players_from_song(Song("Fourth"))) == []
    assert data_viewer.data_store.get_player_lists() == [(1, "A"), (2, "A"), (1, "B")]

    game_manager.reset_tables()
    assert data_viewer.get_current_game() is None

def test_rename():
    game_manager = GameManager()
    data_viewer = DataViewer()
    list_adder = ListAdder()

    game_manager.reset_tables()
    assert data_viewer.get_current_game() is None
    game_manager.start_game("rename")

    list_adder.add_player("A", [Song("1st")])

    assert data_viewer.get_songs() == [Song("1st")]
    assert data_viewer.get_song_index(Song("1st")) == 1
    assert data_viewer.get_song_index(Song("First")) == None

    game_manager.rename_song(Song("1st"), Song("First"))

    assert data_viewer.get_songs() == [Song("First")]
    assert data_viewer.get_song_index(Song("1st")) == None
    assert data_viewer.get_song_index(Song("First")) == 1

    game_manager.reset_tables()
    assert data_viewer.get_current_game() is None