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

    list_adder.add_player("A", ["1", "2"])
    list_adder.add_player("B", ["1", "2"])

    assert set(data_viewer.get_all_players()) == {"A", "B"}
    assert set(data_viewer.get_songs()) == {"1", "2"}
    assert set(data_viewer.get_players("1")) == {"A", "B"}
    assert set(data_viewer.get_players("2")) == {"A", "B"}

    game_manager.start_game("second")

    assert data_viewer.get_current_game() == 2
    assert data_viewer.get_game_prompt(2) == "second"

    list_adder.add_player("A", ["1", "3"])
    list_adder.add_player("C", ["1", "3"])

    assert set(data_viewer.get_all_players()) == {"A", "C"}
    assert set(data_viewer.get_songs()) == {"1", "3"}
    assert set(data_viewer.get_players("1")) == {"A", "C"}
    assert set(data_viewer.get_players("3")) == {"A", "C"}

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
