from cli import CLI, find_arguments

def test_find_arguments():
    assert find_arguments("merge 1 1'") == ("merge", "1 1'")
    assert find_arguments("show-score") == ("show-score", None)
    assert find_arguments("add-list person song 1, song 2") == ("add-list", "person song 1, song 2")

def test_run_command():
    cli = CLI()
    cli.run_command("reset", None)
    cli.run_command("new", "cli test")

    assert cli.run_command("prompt", None) == "cli test"
    assert cli.run_command("songs", None) == ""
    assert cli.run_command("players", None) == ""
    assert cli.run_command("votes", None) == ""

    cli.run_command("list", "1 A-A, B-B")

    assert cli.run_command("songs", None) == "0 - A - A (https://www.youtube.com/results?search_query=A+-+A)\n1 - B - B (https://www.youtube.com/results?search_query=B+-+B)"
    assert cli.run_command("players", None) == "1"
    assert cli.run_command("votes", None) == "A - A: 0\nB - B: 0"

    assert cli.run_command("youtube", "1") == "https://www.youtube.com/results?search_query=B+-+B"

    cli.run_command("list", "2 A-A', C-C'")

    assert cli.run_command("players", None) == "1, 2"
    assert cli.run_command("votes", None) == "A - A: 0\nB - B: 0\nA - A': 0\nC - C': 0"

    cli.run_command("rename", "3 C-C")

    assert cli.run_command("votes", None) == "A - A: 0\nB - B: 0\nA - A': 0\nC - C: 0"

    cli.run_command("merge", "0 2")

    assert cli.run_command("players", None) == "1, 2"
    assert cli.run_command("votes", None) == "A - A: 0\nB - B: 0\nC - C: 0"

    cli.run_command("vote", "0 1")

    assert cli.run_command("votes", None) == "A - A: 1\nB - B: 1\nC - C: 0"

    cli.run_command("vote-by-song", "2 3")

    assert cli.run_command("votes", None) == "A - A: 1\nB - B: 1\nC - C: 3"

    assert cli.run_command("tally", None) == "2 - 2.0\n1 - 0.0"

    assert cli.run_command("detail", "1") == "total: 0.0, songs: {'A - A': {'score': 0.0, 'votes': 1, 'players': 2}, 'B - B': {'score': 0.0, 'votes': 1, 'players': 1}}"
    assert cli.run_command("detail", "2") == "total: 2.0, songs: {'A - A': {'score': 0.0, 'votes': 1, 'players': 2}, 'C - C': {'score': 2.0, 'votes': 3, 'players': 1}}"

    cli.run_command("reset", None)