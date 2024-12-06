from listwrap import align


def test_align() -> None:
    items = ["a", "b"]
    assert align(items) == '    "a",\n    "b",'
    assert align(items, quote="'") == "    'a',\n    'b',"
    assert align(items, sep=" | ") == '    "a" | \n    "b" | '
    assert align(items, vertical=False) == '    "a","b",'
    assert align(items, trailsep=False) == '    "a",\n    "b"'
    assert align(items, indent=2) == '  "a",\n  "b",'
    assert align(items, sep=" | ", vertical=False, trailsep=False, indent=2) == '  "a" | "b"'
