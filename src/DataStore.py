import sqlite3
import sys

from src.Phases import Phase

class DataStore:
    #assuming pytest is only in modules if one is running tests
    database = "test_song_game.db" if "pytest" in sys.modules else "song_game.db"
    connection = sqlite3.connect(database, check_same_thread=False)
    cursor = connection.cursor()

    def __init__(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
	            game_index INTEGER PRIMARY KEY,
                phase TEXT NOT NULL,
   	            prompt TEXT
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                game_index INTEGER NOT NULL,
	            song_name TEXT NOT NULL,
   	            votes INTEGER DEFAULT 0,
                PRIMARY KEY(game_index, song_name)
                FOREIGN KEY(game_index) REFERENCES games(game_index)
            );
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_lists (
                game_index INTEGER NOT NULL,
	            song_name TEXT NOT NULL,
   	            player TEXT NOT NULL,
                FOREIGN KEY(game_index) REFERENCES games(game_index),
                FOREIGN KEY(game_index, song_name) REFERENCES songs(game_index, song_name)
            );
        ''')

    def reset_tables(self):
        self.cursor.execute("DELETE FROM games;")
        self.cursor.execute("DELETE FROM songs;")
        self.cursor.execute("DELETE FROM player_lists;")
        self.connection.commit()

    def get_current_game(self):
        res = self.cursor.execute("SELECT MAX(game_index) FROM games;")
        return res.fetchone()[0]
    
    def get_game_phase(self, game_index: int):
        res = self.cursor.execute("SELECT phase FROM games WHERE game_index='{}';".format(game_index))
        return Phase[res.fetchone()[0]]
    
    def get_game_prompt(self, game_index: int):
        res = self.cursor.execute("SELECT prompt FROM games WHERE game_index='{}';".format(game_index))
        return res.fetchone()[0]
    
    def get_songs(self) -> list[str]:
        game_index = self.get_current_game()
        res = self.cursor.execute("SELECT song_name FROM songs WHERE game_index = {};".format(game_index))
        return map(lambda x: x[0], res.fetchall())
    
    def get_all_players(self) -> list[str]:
        game_index = self.get_current_game()
        res = self.cursor.execute("SELECT DISTINCT player FROM player_lists WHERE game_index = {};".format(game_index))
        return map(lambda x: x[0], res.fetchall())

    def get_players(self, song: str) -> list[str]:
        game_index = self.get_current_game()
        res = self.cursor.execute("SELECT player FROM player_lists WHERE song_name='{}' AND game_index = {};".format(song.replace("'", "''"), game_index))
        return map(lambda x: x[0], res.fetchall())
    
    def get_votes(self, song: str) -> int:
        game_index = self.get_current_game()
        res = self.cursor.execute("SELECT votes FROM songs WHERE song_name='{}' AND game_index = {};".format(song.replace("'", "''"), game_index))
        return res.fetchone()[0]
    
    def get_player_lists(self) -> tuple[str, str]:
        game_index = self.get_current_game()
        res = self.cursor.execute("SELECT song_name, player from player_lists WHERE game_index = {};".format(game_index))
        return res.fetchall()
    
    def start_new_game(self, prompt: str):
        self.cursor.execute("INSERT INTO games (phase, prompt) SELECT 'ADD_LIST', '{}'".format(prompt))
        self.connection.commit()
        return self.get_current_game()
        
    def change_phase(self, game_index: int, phase: Phase):
        self.cursor.execute("UPDATE games SET phase = '{}' WHERE game_index = {}".format(phase.name, game_index))
        self.connection.commit()
    
    def add_player_list(self, player: str, songs: list[str]):
        game_index = self.get_current_game()
        for song in songs:
            self.cursor.execute("INSERT INTO songs (game_index, song_name) SELECT {0}, '{1}' WHERE NOT EXISTS (SELECT 1 FROM songs WHERE game_index = {0} AND song_name = '{1}');".format(game_index, song.replace("'", "''")))
            self.cursor.execute("INSERT INTO player_lists (game_index, song_name, player) SELECT {}, '{}', '{}';".format(game_index, song.replace("'", "''"), player))
        self.connection.commit()

    def add_votes_from_list(self, song_list: list[str]):
        game_index = self.get_current_game()
        sql_song_list = "('" + "','".join(song_list) + "')"
        self.cursor.execute("UPDATE songs SET votes = votes + 1 WHERE song_name IN {} AND game_index = {};".format(sql_song_list, game_index))
        self.connection.commit()

    def add_votes_to_song(self, song: str, votes: int):
        game_index = self.get_current_game()
        self.cursor.execute("UPDATE songs SET votes = votes + {} WHERE song_name = '{}' AND game_index = {};".format(votes, song.replace("'", "''"), game_index))
        self.connection.commit()

    def merge_songs(self, song1:str, song2: str):
        game_index = self.get_current_game()
        self.cursor.execute("UPDATE player_lists SET song_name = '{}' WHERE song_name = '{}' AND game_index = {};".format(song1.replace("'", "''"), song2.replace("'", "''"), game_index))
        self.cursor.execute("DELETE FROM songs WHERE song_name = '{}' AND game_index = {};".format(song2.replace("'", "''"), game_index))
        self.connection.commit()