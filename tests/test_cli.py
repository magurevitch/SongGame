import cli

def test_format_title():
    assert cli.format_title("A-B") == "A - B"
    assert cli.format_title("A-B-C") == "A - B-C"
    assert cli.format_title(" A-B ") == "A - B"
    assert cli.format_title("A   -   B") == "A - B"

def test_find_arguments():
    assert cli.find_arguments("merge 1 1'") == ("merge", "1 1'")
    assert cli.find_arguments("show-score") == ("show-score", None)
    assert cli.find_arguments("add-list person song 1, song 2") == ("add-list", "person song 1, song 2")

def test_youtube():
    song_title = "Barrett's Privateers - Stan Rogers"
    assert cli.get_song_youtube_link(song_title) == "https://www.youtube.com/results?search_query=Barrett%27s+Privateers+-+Stan+Rogers"

def test_run_command():
    cli.run_command("reset", None)

    assert cli.run_command("songs", None) == ""
    assert cli.run_command("players", None) == ""
    assert cli.run_command("votes", None) == ""

    cli.run_command("list", "1 A-A, B-B")

    assert cli.run_command("songs", None) == "0 - A - A (https://www.youtube.com/results?search_query=A+-+A)\n1 - B - B (https://www.youtube.com/results?search_query=B+-+B)"
    assert cli.run_command("players", None) == "1"
    assert cli.run_command("votes", None) == "A - A: 0\nB - B: 0"

    assert cli.run_command("youtube", "1") == "https://www.youtube.com/results?search_query=B+-+B"

    cli.run_command("list", "2 A-A', C-C")

    assert cli.run_command("players", None) == "1, 2"
    assert cli.run_command("votes", None) == "A - A: 0\nA - A': 0\nB - B: 0\nC - C: 0"

    cli.run_command("merge", "0 1")

    assert cli.run_command("players", None) == "1, 2"
    assert cli.run_command("votes", None) == "A - A: 0\nB - B: 0\nC - C: 0"

    cli.run_command("vote", "0 1")

    assert cli.run_command("votes", None) == "A - A: 1\nB - B: 1\nC - C: 0"

    cli.run_command("vote-by-song", "2 3")

    assert cli.run_command("votes", None) == "A - A: 1\nB - B: 1\nC - C: 3"

    assert cli.run_command("tally", None) == "2 - 2.0\n1 - 0.0"

    assert cli.run_command("detail", "1") == "total: 0.0, songs: {'A - A': 0.0, 'B - B': 0.0}"
    assert cli.run_command("detail", "2") == "total: 2.0, songs: {'A - A': 0.0, 'C - C': 2.0}"

    cli.run_command("reset", None)

    assert cli.run_command("songs", None) == ""
    assert cli.run_command("players", None) == ""
    assert cli.run_command("votes", None) == ""