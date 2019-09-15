#!/usr/bin/env python3

import sys
from anagram_groups_finder import AnagramGroupsFinder


if __name__ == "__main__":
    print("Anagram groups are:")
    groups_finder = AnagramGroupsFinder()
    groups_finder.process_from_file(sys.argv[1])
    groups_finder.print_groups()
