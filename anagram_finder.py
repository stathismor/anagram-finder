import shelve
import dbm
import io
from typing import List, Iterator

from anagram_error import (
    AnagramFinderFileNotProvidedError,
    AnagramFinderFileNotFoundError,
)

_DEFAULT_SHELF_FILEPATH = "data/shelf.db"


class AnagramFinder:
    """
    Given a source of words, finds the anagram groups, stores them and provides a
    memory-efficient way to fetch them.
    """

    def __init__(self, shelf_file: str = _DEFAULT_SHELF_FILEPATH):
        self._shelf_file = shelf_file

    def process_from_file(self, words_file: str) -> None:
        """
        Given the filepath of the input file, find the groups and save them on
        the storage.
        """
        if not words_file:
            raise AnagramFinderFileNotProvidedError

        try:
            with open(words_file) as file_object, shelve.open(
                self._shelf_file, "n"
            ) as shelf:
                self._process_file(file_object, shelf)
        except IOError:
            raise AnagramFinderFileNotFoundError

    def _process_file(self, file_object: io.IOBase, shelf: shelve.DbfilenameShelf):
        """
        Parse the file line-by-line, load it in memory, sanitise, and save it.
        """
        for line in file_object:
            word = line.rstrip("\n").rstrip("\r")
            self._save_word(word, shelf)

    def _save_word(self, word: str, shelf: shelve.DbfilenameShelf) -> set:
        """
        Save the word with as key/value pair.

        Two words that are anagrams, will be the same when sorted alphabetically.
        For this reason, we use the sorted word as the key of the anagram groups.
        Every anagram we process will be appended to this key.
        """
        sorted_word = "".join(sorted(word))

        try:
            # NOTE: This will load the whole value in memory
            group = shelf[sorted_word]
        except KeyError:
            # Save as set, to avoid duplicates
            group = set()

        group.add(word)

        shelf[sorted_word] = group

        return shelf[sorted_word]

    def get_groups(self) -> Iterator[List[str]]:
        """
        Yield all groups of the storage.
        """
        try:
            with shelve.open(self._shelf_file, "r") as shelf:
                for key in shelf:
                    yield shelf[key]
        except dbm.error:
            raise AnagramFinderFileNotFoundError

    # Used for testing

    def process_from_text(self, words) -> None:
        """
        To facilitate testing and not use files, provide a text input interface.
        """
        with shelve.open(self._shelf_file, "n", writeback=True) as shelf:
            for word in words:
                self._save_word(word, shelf)
