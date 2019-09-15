from anagram_groups_finder import AnagramGroupsFinder
import shelve


def test_anagram_finder():
    groups_finder = AnagramGroupsFinder(None)
    words = ["abc", "fun", "bac", "fun", "cba", "unf", "hello"]
    word = "abc"

    # with shelve.open("test.db", "n", writeback=True) as shelf:
    groups_finder.save_anagram_groups()

    assert groups_finder.get_anagram_group("abc") == "abc"
