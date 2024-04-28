from src.models.Song import Song

def extract_song(song: str) -> Song:
    if "-" in song:
        song_name, artist = song.split("-", 1)
        return Song(song_name.strip(), artist.strip())
    return Song(song.strip())