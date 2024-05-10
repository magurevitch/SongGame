import asyncio
import time

import pytest

from src.utils import extract_song, lock

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

@pytest.mark.asyncio
async def test_lock():
    class Counter:
        counter = 0

        @lock
        async def increase(self):
            await asyncio.sleep(0.1)
            self.counter += 1

        @lock
        async def decrease(self):
            await asyncio.sleep(0.1)
            self.counter -= 1

    counter = Counter()

    #testing lock stops the same function twice
    await asyncio.gather(counter.increase(), counter.increase())
    assert counter.counter == 1

    #testing lock does not stop two different functions
    await asyncio.gather(counter.increase(), counter.decrease(), counter.decrease())
    assert counter.counter == 1