from src.SongBank import SongBank
from src.DataStore import DataStore

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

def run_command(command: str, arguments: str | None) -> str:
    song_bank = SongBank()
    data_store = DataStore()
    match command:
        case "reset":
            data_store.reset_tables()
            return "all data wiped"
        case "songs":
            songs = list(data_store.get_songs())
            return "\n".join(str(i) + " - " + songs[i] + " (" + get_song_youtube_link(songs[i]) + ")" for i in range(len(songs)))
        case "players":
            players = data_store.get_all_players()
            return ", ".join(players)
        case "votes":
            songs = list(data_store.get_songs())
            return "\n".join(song + ": " + str(data_store.get_votes(song)) for song in songs)
        case "list":
            player, songs = arguments.split(" ", 1)
            song_bank.add_player(player, [format_title(title) for title in songs.split(",")])
            return "added songs for player " + player
        case "merge":
            index1, index2 = arguments.split()
            songs = list(data_store.get_songs())
            song_bank.merge_songs(songs[int(index1)], songs[int(index2)])
            return "merged song {} into song {}".format(songs[int(index1)], songs[int(index2)])
        case "vote":
            votes = set(arguments.split())
            songs = list(data_store.get_songs())
            if len(votes) > len(songs):
                raise IndexError()
            song_bank.add_votes([songs[int(i)] for i in votes])
            return "added votes for {}".format(", ".join(songs[int(i)] for i in votes))
        case "vote-by-song":
            songs = list(data_store.get_songs())
            index, votes = arguments.split()
            song = songs[int(index)]
            data_store.add_votes_to_song(song, int(votes))
            return "song {} now has {} votes".format(song, data_store.get_votes(song))
        case "tally":
            return "\n".join(player + " - " + str(score) for player, score in song_bank.make_tally_board())
        case "detail":
            return str(song_bank.get_detailed_breakdown(arguments))
        case "youtube":
            songs = list(data_store.get_songs())
            song_title = songs[int(arguments)]
            return get_song_youtube_link(song_title)
        case _:
            return "valid commands are stop, reset, songs, players, votes, list, merge, vote, vote-by-song, tally, detail, and youtube"

def run_cli():
    command, arguments = find_arguments(input())
    while command != "stop":
        response = run_command(command, arguments)
        print(response)
        command, arguments = find_arguments(input())

if __name__ == "__main__":
    run_cli()