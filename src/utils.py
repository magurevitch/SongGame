from src.models.Song import Song

def extract_song(song: str) -> Song:
    if "-" in song:
        song_title, artist = song.split("-", 1)
        return Song(song_title.strip(), artist.strip())
    return Song(song.strip())

def lock(function):
    async def wrapper(*args, **kwargs):
        if wrapper.lock:
            print("rejected!")
            return
        wrapper.lock = True
        value = await function(*args, **kwargs)
        wrapper.lock = False
        return value
    wrapper.lock = False
    return wrapper