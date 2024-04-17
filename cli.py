from src.SongBank import SongBank

def format_title(raw_title) -> str:
    song_name, artist = raw_title.split("-", 1)
    return "{} - {}".format(song_name.strip(), artist.strip())

def find_arguments(raw_input):
    command, *arguments = raw_input.split(" ", 1)
    return command.strip(), None if arguments == [] else arguments[0]

def get_song_youtube_link(song_title):
    youtube_format = "https://www.youtube.com/results?search_query="
    cleaned_song_title = song_title.replace(" ", "+").replace("'", "%27")
    return youtube_format + cleaned_song_title

def run_cli():
    song_bank = SongBank()

    def run_command(command, arguments):
        match command:
            case "list":
                player, songs = arguments.split(" ", 1)
                song_bank.add_player(player, [format_title(title) for title in songs.split(",")])
                print("added songs for player", player)
            case "vote":
                votes = set(arguments.split())
                songs = list(song_bank.get_songs())
                if len(votes) > len(songs):
                    raise IndexError()
                song_bank.add_votes([songs[int(i)] for i in votes])
                print("added votes for {}".format(", ".join(songs[int(i)] for i in votes)))
            case "merge":
                index1, index2 = arguments.split()
                songs = list(song_bank.get_songs())
                song_bank.merge_songs(songs[int(index1)], songs[int(index2)])
                print("merged song {} into song {}".format(songs[int(index1)], songs[int(index2)]))
            case "tally":
                for player, score in song_bank.make_tally_board():
                    print(player, score)
            case "detail":
                print(song_bank.get_detailed_breakdown(arguments))
            case "youtube":
                songs = list(song_bank.get_songs())
                song_title = songs[int(arguments)]
                print(get_song_youtube_link(song_title))
            case _:
                return

    command, arguments = find_arguments(input())
    while command != "stop":
        run_command(command, arguments)
        players = song_bank.players
        if players:
            print(", ".join(players))
        songs = list(song_bank.get_songs())
        if songs:
            print("songs:")
            for i in range(len(songs)):
                print(i, "-", songs[i], "(" + get_song_youtube_link(songs[i]) + ")")
        command, arguments = find_arguments(input())

if __name__ == "__main__":
    run_cli()