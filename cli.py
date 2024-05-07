from src.Phases import Phase
from src.DataUsers.GameManager import GameManager
from src.DataUsers.DataViewer import DataViewer
from src.DataUsers.ListAdder import ListAdder
from src.DataUsers.Voter import Voter
from src.DataUsers.Scorer import Scorer
from src.utils import extract_song

commands = {
    "stop": {"phase": None, "arguments": None, "description": "closes the cli"},
    "help": {"phase": None, "arguments": "command_name", "description": "gives the description of given command"}, 
    "reset": {"phase": None, "arguments": None, "description": "resets the databases to be null"},
    "new": {"phase": None, "arguments": "prompt", "description": "starts a new game with the given prompt"},
    "prompt": {"phase": None, "arguments": None, "description": "gets prompt for current game"},
    "phase": {"phase": None, "arguments": None, "description": "gets phase for current game"},
    "advance": {"phase": None, "arguments": None, "description": "advances phase for current game"},
    "songs": {"phase": None, "arguments": None, "description": "lists all songs with index and youtube link"},
    "players": {"phase": None, "arguments": None, "description": "lists all players"},
    "votes": {"phase": None, "arguments": None, "description": "lists all songs with votes"},
    "youtube": {"phase": None, "arguments": "song_index", "description": "gets a link to a youtube search for the song of given index"},
    "list": {"phase": Phase.ADD_LIST, "arguments": "player <comma separated list of song names for the player>", "description": "adds the list for a given player"},
    "rename": {"phase": None, "arguments": "index song_title - artist", "description": "renames song at that index to the new parameters"},
    "merge": {"phase": None, "arguments": "index_1 index_2", "description": "merges the song from index_2 into index_1"},
    "vote": {"phase": Phase.VOTE, "arguments": "space separated list of song indices", "description": "casts a vote for songs of the listed indices" },
    "vote-by-song": {"phase": Phase.VOTE, "arguments": "song_index number_of_votes", "description": "casts multiple votes for the song of the given index"},
    "tally": {"phase": Phase.SCORE, "arguments": None, "description": "gives a tally of players and final votes, ordered from most to least votes"},
    "detail": {"phase": Phase.SCORE, "arguments": "player", "description": "gives a detailed list of which songs gave the given player points"},
    "admin": {"phase": None, "arguments": None, "description": "puts the game in ADMIN phase"}
}

def find_arguments(raw_input:str) -> list[str, None]:
    command, *arguments = raw_input.split(" ", 1)
    return command.strip(), None if arguments == [] else arguments[0]

class CLI:
    def __init__(self):
        self.game_manager = GameManager()
        self.data_viewer = DataViewer()
        self.list_adder = ListAdder()
        self.voter = Voter()
        self.scorer = Scorer()

    def check_phase(self, phase: Phase | None):
        relevant_data_user = {
            Phase.ADD_LIST: self.list_adder,
            Phase.VOTE: self.voter,
            Phase.SCORE: self.scorer,
        }[phase]
        index = self.data_viewer.get_current_game()
        if not relevant_data_user.is_allowed(index):
            print("changing phase to {}".format(phase.name))
            self.game_manager.change_phase(index, phase)
            if phase == Phase.SCORE:
                relevant_data_user.make_scores()

    def run_command(self, command: str, arguments: str | None) -> str:
        if command in commands and commands[command]["phase"]:
            self.check_phase(commands[command]["phase"])
        match command:
            case "help":
                if not arguments:
                    return "valid commands are " + ", ".join(commands.keys())
                command_help = commands[arguments]
                phase = command_help["phase"].name if command_help["phase"] else "All Phases"
                arguments = command_help["arguments"] if command_help["arguments"] else ""
                return "Phase: {}\nArguments: {}\nDescription: {}".format(phase, arguments, command_help["description"])
            case "reset":
                self.game_manager.reset_tables()
                return "all data wiped"
            case "new":
                self.game_manager.start_game(arguments)
                return "started a new game"
            case "prompt":
                game_index = self.data_viewer.get_current_game()
                return self.data_viewer.get_game_prompt(game_index)
            case "phase":
                game_index = self.data_viewer.get_current_game()
                return self.data_viewer.get_game_phase(game_index).name
            case "advance":
                return self.game_manager.advance_current_phase().name
            case "songs":
                songs = list(self.data_viewer.get_songs())
                return "\n".join(str(i) + " - " + str(songs[i]) + " (" + songs[i].get_song_youtube_link() + ")" for i in range(len(songs)))
            case "players":
                players = self.data_viewer.get_all_players()
                return ", ".join(players)
            case "votes":
                songs = list(self.data_viewer.get_songs())
                return "\n".join(str(song) + ": " + str(self.data_viewer.get_votes_from_song(song)) for song in songs)
            case "youtube":
                songs = list(self.data_viewer.get_songs())
                song = songs[int(arguments)]
                return song.get_song_youtube_link()
            case "list":
                player, songs = arguments.split(" ", 1)
                self.list_adder.add_player(player, [extract_song(title) for title in songs.split(",")])
                return "added songs for player " + player
            case "rename":
                songs = list(self.data_viewer.get_songs())
                index, raw_song = arguments.split(" ", 1)
                song = songs[int(index)]
                self.game_manager.rename_song(song, extract_song(raw_song))
            case "merge":
                index1, index2 = arguments.split()
                songs = list(self.data_viewer.get_songs())
                self.game_manager.merge_songs(songs[int(index1)], songs[int(index2)])
                return "merged song {} into song {}".format(songs[int(index1)], songs[int(index2)])
            case "vote":
                votes = set(arguments.split())
                songs = list(self.data_viewer.get_songs())
                if len(votes) > len(songs):
                    raise IndexError()
                self.voter.add_votes([self.data_viewer.get_song_index(songs[int(i)]) for i in votes])
                return "added votes for {}".format(", ".join(str(songs[int(i)]) for i in votes))
            case "vote-by-song":
                songs = list(self.data_viewer.get_songs())
                index, votes = arguments.split()
                song = songs[int(index)]
                index = self.data_viewer.get_song_index(song)
                self.voter.add_votes_to_song(index, int(votes))
                return "song {} now has {} votes".format(song, self.data_viewer.get_votes_from_song(song))
            case "tally":
                return "\n".join(player + " - " + str(score) for player, score in self.scorer.get_tally_board())
            case "detail":
                return str(self.scorer.get_detailed_breakdown(arguments))
            case "admin":
                game_index = self.data_viewer.get_current_game()
                self.game_manager.change_phase(game_index, Phase.ADMIN)
                return "in ADMIN phase"
            case _:
                return "valid commands are " + ", ".join(commands.keys())

    def run_cli(self):
        current_game = self.data_viewer.get_current_game()
        if current_game is None:
            print(self.run_command("new", "") + " with no prompt")
        else:
            print("current prompt is: " + self.run_command("prompt", current_game))
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