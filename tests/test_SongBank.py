from src.SongBank import SongBank
import pytest

def test_song_bank():
    song_bank = SongBank()

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
    song_bank.add_player("B", ["1", "2", "3", "5"])
    #indicating that C has a type in song 1, and so manually merge the typo 1' into 1
    song_bank.add_player("C", ["1'", "3", "6"])

    song_bank.merge_songs("1", "1'")

    assert set(song_bank.players) == {"A", "B", "C"}
    assert set(song_bank.get_songs()) == {"1", "2", "3", "4", "5", "6"}

    song_bank.add_votes(["1", "2", "4"])
    song_bank.add_votes(["1", "2", "3", "4", "5"])
    song_bank.add_votes(["1", "2", "3", "4", "5", "6"])

    assert song_bank.songs["1"].score() == 2/3
    assert song_bank.songs["2"].score() == 1
    assert song_bank.songs["3"].score() == 1/2
    assert song_bank.songs["4"].score() == 2
    assert song_bank.songs["5"].score() == 1
    assert song_bank.songs["6"].score() == 0

    final_score = song_bank.get_score()

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