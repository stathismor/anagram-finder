#!/usr/bin/env python3

import sys
from anagram_finder import AnagramFinder


if __name__ == "__main__":
    finder = AnagramFinder()
    finder.process_from_file(sys.argv[1])

    print("Anagram groups are:")
    for group in finder.get_groups():
        group = ",".join(group)
        print(group)
