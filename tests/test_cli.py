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