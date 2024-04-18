import sqlite3
import sys

class DataStore:
    #assuming pytest is only in modules if one is running tests
    database = "test_song_game.db" if "pytest" in sys.modules else "song_game.db"
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    def __init__(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
	            song_name TEXT PRIMARY KEY,
   	            votes INTEGER DEFAULT 0
            );
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_lists (
	            song_name TEXT NOT NULL,
   	            player TEXT NOT NULL,
                FOREIGN KEY(song_name) REFERENCES songs(song_name)
            );
        ''')
    
    def reset_tables(self):
        self.cursor.execute("DELETE FROM songs;")
        self.cursor.execute("DELETE FROM player_lists;")
        self.connection.commit()
    
    def get_songs(self) -> list[str]:
        res = self.cursor.execute("SELECT song_name FROM songs;")
        return map(lambda x: x[0], res.fetchall())
    
    def get_all_players(self) -> list[str]:
        res = self.cursor.execute("SELECT DISTINCT player FROM player_lists;")
        return map(lambda x: x[0], res.fetchall())

    def get_players(self, song: str) -> str:
        res = self.cursor.execute("SELECT player FROM player_lists WHERE song_name='{}';".format(song.replace("'", "''")))
        return map(lambda x: x[0], res.fetchall())
    
    def get_votes(self, song: str) -> int:
        res = self.cursor.execute("SELECT votes FROM songs WHERE song_name='{}';".format(song.replace("'", "''")))
        return res.fetchone()[0]
    
    def get_player_lists(self) -> tuple[str, str]:
        res = self.cursor.execute("SELECT song_name, player from player_lists;")
        return res.fetchall()
    
    def add_player_list(self, player: str, songs: list[str]):
        for song in songs:
            self.cursor.execute("INSERT INTO songs (song_name) SELECT '{0}' WHERE NOT EXISTS (SELECT 1 FROM songs WHERE song_name = '{0}');".format(song.replace("'", "''")))
            self.cursor.execute("INSERT INTO player_lists (song_name, player) SELECT '{}', '{}';".format(song.replace("'", "''"), player))
        self.connection.commit()

    def add_votes_from_list(self, song_list: list[str]):
        sql_song_list = "('" + "','".join(song_list) + "')"
        self.cursor.execute("UPDATE songs SET votes = votes + 1 WHERE song_name IN {};".format(sql_song_list))
        self.connection.commit()

    def add_votes_to_song(self, song: str, votes: int):
        self.cursor.execute("UPDATE songs SET votes = votes + {} WHERE song_name = '{}';".format(votes, song.replace("'", "''")))
        self.connection.commit()

    def merge_songs(self, song1:str, song2: str):
        self.cursor.execute("UPDATE player_lists SET song_name = '{}' WHERE song_name = '{}';".format(song1.replace("'", "''"), song2.replace("'", "''")))
        self.cursor.execute("DELETE FROM songs WHERE song_name = '{}';".format(song2.replace("'", "''")))
        self.connection.commit()