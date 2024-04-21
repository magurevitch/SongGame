import sqlite3
import sys

from src.Phases import Phase

def for_db(text: str) -> str:
    return text.replace("'", "''")

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
                game_index INTEGER NOT NULL,
	            song_name TEXT NOT NULL,
   	            votes INTEGER DEFAULT 0,
                PRIMARY KEY(game_index, song_name)
                FOREIGN KEY(game_index) REFERENCES games(game_index)
            );
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_lists (
                game_index INTEGER NOT NULL,
	            song_name TEXT NOT NULL,
   	            player TEXT NOT NULL,
                FOREIGN KEY(game_index) REFERENCES games(game_index),
                FOREIGN KEY(game_index, song_name) REFERENCES songs(game_index, song_name)
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
        res = cursor.execute(query)
        return res.fetchone()[0]
    
    def fetch_many_values(self, query: str):
        cursor = self.connection.cursor()
        res = cursor.execute(query)
        return map(lambda x: x[0], res.fetchall())

    def get_current_game(self) -> int:
        return self.fetch_single_value("SELECT MAX(game_index) FROM games;")
    
    def get_game_phase(self, game_index: int) -> Phase:
        phase = self.fetch_single_value("SELECT phase FROM games WHERE game_index='{}';".format(game_index))
        return Phase[phase]
    
    def get_game_prompt(self, game_index: int) -> str:
        return self.fetch_single_value("SELECT prompt FROM games WHERE game_index='{}';".format(game_index))
    
    def get_songs(self) -> list[str]:
        game_index = self.get_current_game()
        return self.fetch_many_values("SELECT song_name FROM songs WHERE game_index = {};".format(game_index))
    
    def get_all_players(self) -> list[str]:
        game_index = self.get_current_game()
        return self.fetch_many_values("SELECT DISTINCT player FROM player_lists WHERE game_index = {};".format(game_index))

    def get_players(self, song: str) -> list[str]:
        game_index = self.get_current_game()
        return self.fetch_many_values("SELECT player FROM player_lists WHERE song_name='{}' AND game_index = {};".format(for_db(song), game_index))
    
    def get_votes(self, song: str) -> int:
        game_index = self.get_current_game()
        return self.fetch_single_value("SELECT votes FROM songs WHERE song_name='{}' AND game_index = {};".format(for_db(song), game_index))
    
    def get_player_lists(self) -> list[tuple[str, str]]:
        game_index = self.get_current_game()
        cursor = self.connection.cursor()
        res = cursor.execute("SELECT song_name, player from player_lists WHERE game_index = {};".format(game_index))
        return res.fetchall()
    
    def start_new_game(self, prompt: str):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO games (phase, prompt) SELECT 'ADD_LIST', '{}'".format(prompt))
        self.connection.commit()
        return self.get_current_game()
        
    def change_phase(self, game_index: int, phase: Phase):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE games SET phase = '{}' WHERE game_index = {}".format(phase.name, game_index))
        self.connection.commit()
    
    def add_player_list(self, player: str, songs: list[str]):
        game_index = self.get_current_game()
        cursor = self.connection.cursor()
        for song in songs:
            cursor.execute("INSERT INTO songs (game_index, song_name) SELECT {0}, '{1}' WHERE NOT EXISTS (SELECT 1 FROM songs WHERE game_index = {0} AND song_name = '{1}');".format(game_index, for_db(song)))
            cursor.execute("INSERT INTO player_lists (game_index, song_name, player) SELECT {}, '{}', '{}';".format(game_index, for_db(song), player))
        self.connection.commit()

    def add_votes_from_list(self, song_list: list[str]):
        game_index = self.get_current_game()
        sql_song_list = "('" + "','".join(song_list) + "')"
        cursor = self.connection.cursor()
        cursor.execute("UPDATE songs SET votes = votes + 1 WHERE song_name IN {} AND game_index = {};".format(sql_song_list, game_index))
        self.connection.commit()

    def add_votes_to_song(self, song: str, votes: int):
        game_index = self.get_current_game()
        cursor = self.connection.cursor()
        cursor.execute("UPDATE songs SET votes = votes + {} WHERE song_name = '{}' AND game_index = {};".format(votes, for_db(song), game_index))
        self.connection.commit()

    def merge_songs(self, song1:str, song2: str):
        game_index = self.get_current_game()
        cursor = self.connection.cursor()
        cursor.execute("UPDATE player_lists SET song_name = '{}' WHERE song_name = '{}' AND game_index = {};".format(for_db(song1), for_db(song2), game_index))
        cursor.execute("DELETE FROM songs WHERE song_name = '{}' AND game_index = {};".format(for_db(song2), game_index))
        self.connection.commit()