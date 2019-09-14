import shelve


class AnagramGroupsFinder:
    def __init__(self, words_file: str, shelf_file: str = "data/shelf.db"):
        self._words_file = words_file
        self._shelf_file = shelf_file

    def save_anagram_groups(self) -> None:
        with open(self._words_file) as f, shelve.open(
            self._shelf_file, "n", writeback=True
        ) as shelf:
            for line in f:
                word = line.rstrip("\n").rstrip("\r")
                sorted_word = "".join(sorted(word))

                if sorted_word in shelf:
                    shelf[sorted_word].append(word)
                else:
                    shelf[sorted_word] = [word]

    def print_anagram_groups(self) -> None:
        with shelve.open(self._shelf_file, "r") as shelf:
            for key in shelf:
                group = ",".join(shelf[key])
                print(group)
