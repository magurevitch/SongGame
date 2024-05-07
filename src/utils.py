from src.models.Song import Song

def extract_song(song: str) -> Song:
    if "-" in song:
        song_title, artist = song.split("-", 1)
        return Song(song_title.strip(), artist.strip())
    return Song(song.strip())