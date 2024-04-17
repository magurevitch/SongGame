from src.DataStore import DataStore
from src.ListAdder import ListAdder
from src.Voter import Voter
from src.Scorer import Scorer
from enum import Enum

Phase = Enum('Phase', ['ADD_LIST', 'VOTE', 'SCORE'])

def format_title(raw_title: str) -> str:
    song_name, artist = raw_title.split("-", 1)
    return "{} - {}".format(song_name.strip(), artist.strip())

def find_arguments(raw_input:str) -> list[str, None]:
    command, *arguments = raw_input.split(" ", 1)
    return command.strip(), None if arguments == [] else arguments[0]

def get_song_youtube_link(song_title: str) -> str:
    youtube_format = "https://www.youtube.com/results?search_query="
    cleaned_song_title = song_title.replace(" ", "+").replace("'", "%27")
    return youtube_format + cleaned_song_title

class CLI:
    def __init__(self, is_test=False):
        self.is_test = is_test
        self.data_store = DataStore(is_test)
        self.phase = None
        self.check_phase(Phase.ADD_LIST)

    def check_phase(self, phase: Phase):
        if self.phase != phase:
            print("changing phases from {} to {}".format(self.phase, phase))
            self.phase = phase
            match phase:
                case Phase.ADD_LIST:
                    self.list_adder = ListAdder(self.is_test)
                    self.voter = None
                    self.scorer = None
                case Phase.VOTE:
                    self.list_adder = None
                    self.voter = Voter(self.is_test)
                    self.scorer = None
                case Phase.SCORE:
                    self.list_adder = None
                    self.voter = None
                    self.scorer = Scorer(self.is_test)

    def run_command(self, command: str, arguments: str | None) -> str:
        match command:
            case "reset":
                self.data_store.reset_tables()
                return "all data wiped"
            case "songs":
                songs = list(self.data_store.get_songs())
                return "\n".join(str(i) + " - " + songs[i] + " (" + get_song_youtube_link(songs[i]) + ")" for i in range(len(songs)))
            case "players":
                players = self.data_store.get_all_players()
                return ", ".join(players)
            case "votes":
                songs = list(self.data_store.get_songs())
                return "\n".join(song + ": " + str(self.data_store.get_votes(song)) for song in songs)
            case "list":
                self.check_phase(Phase.ADD_LIST)
                player, songs = arguments.split(" ", 1)
                self.list_adder.add_player(player, [format_title(title) for title in songs.split(",")])
                return "added songs for player " + player
            case "merge":
                self.check_phase(Phase.ADD_LIST)
                index1, index2 = arguments.split()
                songs = list(self.data_store.get_songs())
                self.list_adder.merge_songs(songs[int(index1)], songs[int(index2)])
                return "merged song {} into song {}".format(songs[int(index1)], songs[int(index2)])
            case "vote":
                self.check_phase(Phase.VOTE)
                votes = set(arguments.split())
                songs = list(self.data_store.get_songs())
                if len(votes) > len(songs):
                    raise IndexError()
                self.voter.add_votes([songs[int(i)] for i in votes])
                return "added votes for {}".format(", ".join(songs[int(i)] for i in votes))
            case "vote-by-song":
                self.check_phase(Phase.VOTE)
                songs = list(self.data_store.get_songs())
                index, votes = arguments.split()
                song = songs[int(index)]
                self.voter.add_votes_to_song(song, int(votes))
                return "song {} now has {} votes".format(song, self.data_store.get_votes(song))
            case "tally":
                self.check_phase(Phase.SCORE)
                return "\n".join(player + " - " + str(score) for player, score in self.scorer.make_tally_board())
            case "detail":
                self.check_phase(Phase.SCORE)
                return str(self.scorer.get_detailed_breakdown(arguments))
            case "youtube":
                songs = list(self.data_store.get_songs())
                song_title = songs[int(arguments)]
                return get_song_youtube_link(song_title)
            case _:
                return "valid commands are stop, reset, songs, players, votes, list, merge, vote, vote-by-song, tally, detail, and youtube"

    def run_cli(self):
        print("players: " + self.run_command("players", None))
        print("songs and votes:")
        print(self.run_command("votes", None))
        command, arguments = find_arguments(input())
        while command != "stop":
            response = self.run_command(command, arguments)
            print(response)
            command, arguments = find_arguments(input())

if __name__ == "__main__":
    CLI().run_cli()