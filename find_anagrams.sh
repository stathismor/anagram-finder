#!/usr/bin/env python3

import sys
from anagram_groups_finder import AnagramGroupsFinder


if __name__ == "__main__":
    print("Groups are:", sys.argv)
    groups_finder = AnagramGroupsFinder(sys.argv[1])
    groups_finder.save_anagram_groups()
    groups_finder.print_anagram_groups()
