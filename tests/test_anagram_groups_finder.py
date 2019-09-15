import pytest
from unittest.mock import patch, mock_open
from io import StringIO

from anagram_groups_finder import AnagramGroupsFinder
from anagram_groups_error import (
    AnagramGroupsFinderFileNotProvidedError,
    AnagramGroupsFinderFileNotFoundError,
)


def test_process_from_file_none():
    groups_finder = AnagramGroupsFinder()
    with pytest.raises(AnagramGroupsFinderFileNotProvidedError):
        groups_finder.process_from_file(None)


def test_process_from_file_wrong_file():
    groups_finder = AnagramGroupsFinder()
    with pytest.raises(AnagramGroupsFinderFileNotFoundError):
        groups_finder.process_from_file("/wrong/directory/file.txt")


def test_get_groups_wrong_file():
    groups_finder = AnagramGroupsFinder(shelf_file="/wrong/directory/file.txt")
    with pytest.raises(AnagramGroupsFinderFileNotFoundError):
        list(groups_finder._get_groups())


def test_process_from_file_success():
    """
    Just a sanity check that processing words from file works and does not blow up
    """
    words_file_data = "abc\nfun\nbac\nfun\ncba\nunf\nhello\n"

    groups_finder = AnagramGroupsFinder()
    with patch("builtins.open", mock_open(read_data=words_file_data)) as mock_file:
        groups_finder.process_from_file("/wrong/directory/file.txt")

    expected = [["abc", "bac", "cba"], ["fun", "unf"], ["hello"]]

    assert [sorted(g) for g in groups_finder._get_groups()] == expected


@patch("sys.stdout", new_callable=StringIO)
def test_print_groups_success(mock_stdout):
    """
    Sanity check that print_groups does not blow up. Patch stdout so that
    underlying print does not show up in test console.
    """
    input_words = ["abc", "fun", "bac", "fun", "cba", "unf", "hello"]
    groups_finder = AnagramGroupsFinder()
    groups_finder.process_from_text(input_words)

    groups_finder.print_groups()


def test_get_groups_process_from_text_space():
    """
    Words with space prefixed or suffixed
    """
    input_words = ["a ", " b"]
    groups_finder = AnagramGroupsFinder()
    groups_finder.process_from_text(input_words)

    expected = [["a "], [" b"]]

    assert [sorted(g) for g in groups_finder._get_groups()] == expected


def test_get_groups_process_from_text_one_word():
    input_words = ["abc"]
    groups_finder = AnagramGroupsFinder()
    groups_finder.process_from_text(input_words)

    # There should be only one set, no need to sort, check it's the expected set
    assert next(groups_finder._get_groups(), None) == {"abc"}


def test_get_groups_process_from_text_one_group():
    """
    All the words in the text are the of same group
    """
    input_words = ["abcd", "acbd", "abdc", "bacd", "badc"]
    groups_finder = AnagramGroupsFinder()
    groups_finder.process_from_text(input_words)

    expected = [["abcd", "abdc", "acbd", "bacd", "badc"]]

    assert [sorted(g) for g in groups_finder._get_groups()] == expected


def test_get_groups_process_from_text_different_groups():
    """
    All the words in the text are of different groups
    """
    input_words = ["a", "bc", "efg", "hijk", "klmno", "pqrstuv"]
    groups_finder = AnagramGroupsFinder()
    groups_finder.process_from_text(input_words)

    expected = [{"bc"}, {"a"}, {"klmno"}, {"efg"}, {"hijk"}, {"pqrstuv"}]

    assert list(groups_finder._get_groups()) == expected


def test_get_groups_process_from_text_success():
    input_words = ["abc", "fun", "bac", "fun", "cba", "unf", "hello"]
    groups_finder = AnagramGroupsFinder()
    groups_finder.process_from_text(input_words)

    expected = [["abc", "bac", "cba"], ["fun", "unf"], ["hello"]]

    assert [sorted(g) for g in groups_finder._get_groups()] == expected
