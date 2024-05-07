import sqlite3
import sys

from src.models.Song import Song
from src.Phases import Phase

def for_db(text: str) -> str:
    if text is None:
        return "NULL"
    return "'" + text.replace("'", "''") + "'"

class DataStore:
    #assuming pytest is only in modules if one is running tests
    database = "test_song_game.db" if "pytest" in sys.modules else "song_game.db"
    connection = sqlite3.connect(database, check_same_thread=False)

    def __init__(self):
        cursor = self.connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
	            game_index INTEGER PRIMARY KEY,
                phase TEXT NOT NULL,
   	            prompt TEXT
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                song_index INTEGER PRIMARY KEY,
                game_index INTEGER NOT NULL,
	            song_name TEXT NOT NULL,
                artist TEXT,
   	            votes INTEGER DEFAULT 0,
                FOREIGN KEY(game_index) REFERENCES games(game_index)
            );
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_lists (
                game_index INTEGER NOT NULL,
	            song_index INTEGER NOT NULL,
   	            player TEXT NOT NULL,
                FOREIGN KEY(game_index) REFERENCES games(game_index),
                FOREIGN KEY(song_index) REFERENCES songs(song_index)
            );
        ''')

    def reset_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM games;")
        cursor.execute("DELETE FROM songs;")
        cursor.execute("DELETE FROM player_lists;")
        self.connection.commit()

    def fetch_single_value(self, query: str):
        cursor = self.connection.cursor()
        res = cursor.execute(query).fetchone()
        return res[0] if res is not None else None
    
    def fetch_many_values(self, query: str):
        cursor = self.connection.cursor()
        res = cursor.execute(query).fetchall()
        return map(lambda x: x[0], res)

    def get_current_game(self) -> int:
        return self.fetch_single_value("SELECT MAX(game_index) FROM games;")
    
    def get_game_phase(self, game_index: int) -> Phase:
        phase = self.fetch_single_value("SELECT phase FROM games WHERE game_index='{}';".format(game_index))
        return Phase[phase]
    
    def get_game_prompt(self, game_index: int) -> str:
        return self.fetch_single_value("SELECT prompt FROM games WHERE game_index='{}';".format(game_index))
    
    def get_song_index(self, game_index: int, song: Song) -> int:
        artist_query = "" if song.artist is None else " AND artist = {}".format(for_db(song.artist))
        sql_query = "SELECT song_index FROM songs WHERE game_index = {} AND song_name = {}{}".format(game_index, for_db(song.song_title), artist_query)
        return self.fetch_single_value(sql_query)
    
    def get_all_song_indices(self) -> list[int]:
        game_index = self.get_current_game()
        return self.fetch_many_values("SELECT song_index FROM songs WHERE game_index = {};".format(game_index))
    
    def get_song_details(self, song_index: int) -> Song:
        cursor = self.connection.cursor()
        res = cursor.execute("SELECT song_name, artist FROM songs WHERE song_index = {};".format(song_index))
        song_name, artist = res.fetchone()
        return Song(song_name, artist)
    
    def get_all_players(self) -> list[str]:
        game_index = self.get_current_game()
        return self.fetch_many_values("SELECT DISTINCT player FROM player_lists WHERE game_index = {};".format(game_index))

    def get_players(self, song_index: int) -> list[str]:
        return self.fetch_many_values("SELECT DISTINCT player FROM player_lists WHERE song_index={};".format(song_index))
    
    def get_votes(self, song_index: int) -> int:
        return self.fetch_single_value("SELECT votes FROM songs WHERE song_index = {};".format(song_index))
    
    def get_player_lists(self) -> list[tuple[int, str]]:
        game_index = self.get_current_game()
        cursor = self.connection.cursor()
        res = cursor.execute("SELECT DISTINCT song_index, player from player_lists WHERE game_index = {};".format(game_index))
        return res.fetchall()
    
    def start_new_game(self, prompt: str):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO games (phase, prompt) SELECT 'ADD_LIST', {}".format(for_db(prompt)))
        self.connection.commit()
        return self.get_current_game()
        
    def change_phase(self, game_index: int, phase: Phase):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE games SET phase = '{}' WHERE game_index = {}".format(phase.name, game_index))
        self.connection.commit()
    
    def add_player_list(self, player: str, songs: list[Song]):
        game_index = self.get_current_game()
        cursor = self.connection.cursor()
        for song in songs:
            song_index = self.get_song_index(game_index, song)
            if not song_index:
                song_index = self.fetch_single_value("INSERT INTO songs (game_index, song_name, artist) SELECT {}, {}, {} RETURNING song_index;".format(game_index, for_db(song.song_title), for_db(song.artist)))
            cursor.execute("INSERT INTO player_lists (game_index, song_index, player) SELECT {}, {}, '{}';".format(game_index, song_index, player))
        self.connection.commit()

    def add_votes_from_list(self, song_list: list[int]):
        game_index = self.get_current_game()
        sql_song_list = "(" + ",".join(str(index) for index in song_list) + ")"
        cursor = self.connection.cursor()
        cursor.execute("UPDATE songs SET votes = votes + 1 WHERE song_index IN {} AND game_index = {};".format(sql_song_list, game_index))
        self.connection.commit()

    def add_votes_to_song(self, song_index: int, votes: int):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE songs SET votes = votes + {} WHERE song_index = {};".format(votes, song_index))
        self.connection.commit()

    def rename_song(self, song_index: int, new_song: Song):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE songs SET song_name='{}', artist={} WHERE song_index={};".format(new_song.song_title, "'" + new_song.artist + "'" if new_song.artist else "NULL", song_index))
        self.connection.commit()

    def merge_songs(self, source_song: int, target_song: int):
        game_index = self.get_current_game()
        cursor = self.connection.cursor()
        cursor.execute("UPDATE player_lists SET song_index = {} WHERE song_index = {} AND game_index = {};".format(source_song, target_song, game_index))
        cursor.execute("DELETE FROM songs WHERE song_index = {};".format(target_song))
        self.connection.commit()