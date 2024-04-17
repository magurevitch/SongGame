from src.DataStore import DataStore
from src.SongBank import SongBank
import pytest

def test_song_bank():
    data_store = DataStore(True)
    data_store.reset_tables()
    assert set(data_store.get_songs()) == set()
    assert set(data_store.get_all_players()) == set()
    assert set(data_store.get_player_lists()) == set()
    song_bank = SongBank(True)

    assert song_bank.get_score() == {}

    '''
    songs:
    song 1: on 3 lists, 3 votes
    song 2: on 2 lists, 3 votes
    song 3: on 2 lists, 2 votes
    song 4: on 1 list, 3 votes
    song 5: on 1 list, 2 votes
    song 6: on 1 list, 1 vote  
    '''

    song_bank.add_player("A", ["1", "2", "4"])
    assert set(data_store.get_players("1")) == {"A"}
    assert set(data_store.get_players("2")) == {"A"}
    assert set(data_store.get_players("3")) == set()
    assert set(data_store.get_players("4")) == {"A"}
    assert set(data_store.get_players("5")) == set()
    assert set(data_store.get_players("6")) == set()
    song_bank.add_player("B", ["1", "2", "3", "5"])
    assert set(data_store.get_players("1")) == {"A", "B"}
    assert set(data_store.get_players("2")) == {"A", "B"}
    assert set(data_store.get_players("3")) == {"B"}
    assert set(data_store.get_players("4")) == {"A"}
    assert set(data_store.get_players("5")) == {"B"}
    assert set(data_store.get_players("6")) == set()
    #indicating that C has a type in song 1, and so manually merge the typo 1' into 1
    song_bank.add_player("C", ["1'", "3", "6"])
    assert set(data_store.get_players("1")) == {"A", "B"}
    assert set(data_store.get_players("1'")) == {"C"}
    song_bank.merge_songs("1", "1'")
    assert set(data_store.get_players("1")) == {"A", "B", "C"}
    assert set(data_store.get_players("2")) == {"A", "B"}
    assert set(data_store.get_players("3")) == {"B", "C"}
    assert set(data_store.get_players("4")) == {"A"}
    assert set(data_store.get_players("5")) == {"B"}
    assert set(data_store.get_players("6")) == {"C"}

    assert set(data_store.get_all_players()) == {"A", "B", "C"}
    assert set(data_store.get_songs()) == {"1", "2", "3", "4", "5", "6"}

    song_bank.add_votes(["1", "2", "4"])
    assert data_store.get_votes("1") == 1
    assert data_store.get_votes("2") == 1
    assert data_store.get_votes("3") == 0
    assert data_store.get_votes("4") == 1
    assert data_store.get_votes("5") == 0
    assert data_store.get_votes("6") == 0
    song_bank.add_votes(["1", "2", "3", "4", "5"])
    assert data_store.get_votes("1") == 2
    assert data_store.get_votes("2") == 2
    assert data_store.get_votes("3") == 1
    assert data_store.get_votes("4") == 2
    assert data_store.get_votes("5") == 1
    assert data_store.get_votes("6") == 0
    song_bank.add_votes(["1", "2", "3", "4", "5", "6"])
    assert data_store.get_votes("1") == 3
    assert data_store.get_votes("2") == 3
    assert data_store.get_votes("3") == 2
    assert data_store.get_votes("4") == 3
    assert data_store.get_votes("5") == 2
    assert data_store.get_votes("6") == 1

    final_score = song_bank.get_score()

    assert song_bank.song_scores["1"] == 2/3
    assert song_bank.song_scores["2"] == 1
    assert song_bank.song_scores["3"] == 1/2
    assert song_bank.song_scores["4"] == 2
    assert song_bank.song_scores["5"] == 1
    assert song_bank.song_scores["6"] == 0

    assert "A" in final_score
    assert set(final_score["A"].songs.keys()) == {"1", "2", "4"}
    assert final_score["A"].songs["1"] == 2/3
    assert final_score["A"].songs["2"] == 1
    assert final_score["A"].songs["4"] == 2
    assert final_score["A"].total == 11/3

    assert "B" in final_score
    assert set(final_score["B"].songs.keys()) == {"1", "2", "3", "5"}
    assert final_score["B"].songs["1"] == 2/3
    assert final_score["B"].songs["2"] == 1
    assert final_score["B"].songs["3"] == 1/2
    assert final_score["B"].songs["5"] == 1
    assert final_score["B"].total == 19/6

    assert "C" in final_score
    assert set(final_score["C"].songs.keys()) == {"1", "3", "6"}
    assert final_score["C"].songs["1"] == 2/3
    assert final_score["C"].songs["3"] == 1/2
    assert final_score["C"].songs["6"] == 0
    assert final_score["C"].total == pytest.approx(7/6)
    
    assert song_bank.make_tally_board() == [("A", 11/3), ("B", 19/6), ("C", pytest.approx(7/6))]

    data_store.reset_tables()
    assert set(data_store.get_songs()) == set()
    assert set(data_store.get_all_players()) == set()
    assert set(data_store.get_player_lists()) == set()