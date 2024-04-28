from src.utils import extract_song

def test_extract():
    song = extract_song("title")
    assert song.song_title == "title"
    assert song.artist is None
    assert str(song) == "title - Unknown"

    song = extract_song("title - artist")
    assert song.song_title == "title"
    assert song.artist == "artist"
    assert str(song) == "title - artist"

    song = extract_song(" title-artist ")
    assert song.song_title == "title"
    assert song.artist == "artist"
    assert str(song) == "title - artist"

def test_youtube():
    song_title = "Barrett's Privateers - Stan Rogers"
    song = extract_song(song_title)
    assert song.get_song_youtube_link() == "https://www.youtube.com/results?search_query=Barrett%27s+Privateers+-+Stan+Rogers"
