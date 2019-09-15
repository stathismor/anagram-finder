import shelve
import dbm
import io
from typing import List, Iterator

from anagram_groups_error import (
    AnagramGroupsFinderFileNotProvidedError,
    AnagramGroupsFinderFileNotFoundError,
)

_DEFAULT_SHELF_FILEPATH = "data/shelf.db"


class AnagramGroupsFinder:
    def __init__(self, shelf_file: str = _DEFAULT_SHELF_FILEPATH):
        self._shelf_file = shelf_file

    def process_from_file(self, words_file: str) -> None:
        if not words_file:
            raise AnagramGroupsFinderFileNotProvidedError

        try:
            with open(words_file) as file_object, shelve.open(
                self._shelf_file, "n"
            ) as shelf:
                self._process_file(file_object, shelf)
        except IOError:
            raise AnagramGroupsFinderFileNotFoundError

    def print_groups(self) -> None:
        for group in self._get_groups():
            group = ",".join(group)
            print(group)

    def _process_file(self, file_object: io.IOBase, shelf: shelve.DbfilenameShelf):
        for line in file_object:
            word = line.rstrip("\n").rstrip("\r")
            self._save_line(word, shelf)

    def _save_line(self, word: str, shelf: shelve.DbfilenameShelf) -> set:
        sorted_word = "".join(sorted(word))

        try:
            group = shelf[sorted_word]
        except KeyError:
            group = set()

        group.add(word)

        shelf[sorted_word] = group

        return shelf[sorted_word]

    def _get_groups(self) -> Iterator[List[str]]:
        try:
            with shelve.open(self._shelf_file, "r") as shelf:
                for key in shelf:
                    yield shelf[key]
        except dbm.error:
            raise AnagramGroupsFinderFileNotFoundError

    # Used for testing

    def process_from_text(self, words) -> None:
        with shelve.open(self._shelf_file, "n", writeback=True) as shelf:
            for word in words:
                self._save_line(word, shelf)
