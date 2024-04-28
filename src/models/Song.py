class Song:
    def __init__(self, song_title: str, artist: str = None):
        self.song_title = song_title
        self.artist = artist

    def to_dict(self):
        {"song_title": self.song_title, "artist": self.artist}

    def __str__(self) -> str:
        return self.song_title + " - " + (self.artist if self.artist else "Unknown")

    def __eq__(self, value: object) -> bool:
        return self.song_title == value.song_title and self.artist == value.artist
    
    def get_song_youtube_link(self) -> str:
        youtube_format = "https://www.youtube.com/results?search_query="
        cleaned_song_title = str(self).replace(" ", "+").replace("'", "%27")
        return youtube_format + cleaned_song_title
