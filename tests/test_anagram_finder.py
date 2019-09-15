import pytest
from unittest.mock import patch, mock_open

from anagram_finder import AnagramFinder
from anagram_error import (
    AnagramFinderFileNotProvidedError,
    AnagramFinderFileNotFoundError,
)


@pytest.fixture
def anagram_finder():
    return AnagramFinder()


def test_process_from_file_none(anagram_finder):
    with pytest.raises(AnagramFinderFileNotProvidedError):
        anagram_finder.process_from_file(None)


def test_process_from_file_wrong_file(anagram_finder):
    """
    Input file is wrong.
    """
    with pytest.raises(AnagramFinderFileNotFoundError):
        anagram_finder.process_from_file("/wrong/directory/file.txt")


def test_get_groups_wrong_file(anagram_finder):
    """
    shelve file (used internally) is wrong.
    """
    anagram_finder = AnagramFinder(shelf_file="/wrong/directory/shelf.db")
    with pytest.raises(AnagramFinderFileNotFoundError):
        list(anagram_finder.get_groups())


def test_process_from_file_success(anagram_finder):
    """
    Just a sanity check that processing words from file works and does not blow up
    """
    words_file_data = "abc\nfun\nbac\nfun\ncba\nunf\nhello\n"

    with patch("builtins.open", mock_open(read_data=words_file_data)) as mock_file:
        anagram_finder.process_from_file("/wrong/directory/file.txt")

    expected = [["abc", "bac", "cba"], ["fun", "unf"], ["hello"]]

    assert [sorted(g) for g in anagram_finder.get_groups()] == expected


def test_get_groups_process_from_text_space(anagram_finder):
    """
    Words with space prefixed or suffixed
    """
    input_words = ["a ", " b"]
    anagram_finder.process_from_text(input_words)

    expected = [["a "], [" b"]]

    assert [sorted(g) for g in anagram_finder.get_groups()] == expected


def test_get_groups_process_from_text_empty(anagram_finder):
    """
    Empty words are returned as their own group
    """
    input_words = ["a", "", ""]
    anagram_finder.process_from_text(input_words)

    expected = [["a"], [""]]

    assert [sorted(g) for g in anagram_finder.get_groups()] == expected


def test_get_groups_process_from_text_one_word(anagram_finder):
    input_words = ["abc"]
    anagram_finder.process_from_text(input_words)

    # There should be only one set, no need to sort, just check it's the expected set.
    assert next(anagram_finder.get_groups(), None) == {"abc"}


def test_get_groups_process_from_text_one_group(anagram_finder):
    """
    All the words are of same group.
    """
    input_words = ["abcd", "acbd", "abdc", "bacd", "badc"]
    anagram_finder.process_from_text(input_words)

    expected = [["abcd", "abdc", "acbd", "bacd", "badc"]]

    assert [sorted(g) for g in anagram_finder.get_groups()] == expected


def test_get_groups_process_from_text_different_groups(anagram_finder):
    """
    All the words are of different groups.
    """
    input_words = ["a", "bc", "efg", "hijk", "klmno", "pqrstuv"]
    anagram_finder.process_from_text(input_words)

    expected = [{"bc"}, {"a"}, {"klmno"}, {"efg"}, {"hijk"}, {"pqrstuv"}]

    assert list(anagram_finder.get_groups()) == expected


def test_get_groups_process_from_text_letters_and_numbers(anagram_finder):
    input_words = ["a", "12", "21", "3"]
    anagram_finder.process_from_text(input_words)

    expected = [["3"], ["a"], ["12", "21"]]

    assert [sorted(g) for g in anagram_finder.get_groups()] == expected


def test_get_groups_process_from_text_unicode(anagram_finder):
    input_words = ["a", "\xc2"]
    anagram_finder.process_from_text(input_words)

    expected = [{"\xc2"}, {"a"}]

    assert list(anagram_finder.get_groups()) == expected


def test_get_groups_process_from_text_success(anagram_finder):
    """
    Typical happy path.
    """
    input_words = ["abc", "fun", "bac", "fun", "cba", "unf", "hello"]
    anagram_finder.process_from_text(input_words)

    expected = [["abc", "bac", "cba"], ["fun", "unf"], ["hello"]]

    assert [sorted(g) for g in anagram_finder.get_groups()] == expected
