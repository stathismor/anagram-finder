# Anagram Finder

Given a path to a file with words, find the groups of anagrams.

## Setup

In a virtual env:

```
$ pip install -r requirements.txt
```

(or `pip-sync` if you have `pip-tools`)

## Run anagram finder

`cd` to the root directory and:

```
$ ./run_anagram_finder.py data/example1.txt
Anagram groups are:
abc,bac,cba
unf,fun
hello
```

You can change the input file as you wish.

The anagram finder will find the anagram groups and print them on the standard output, as csv.

## Run tests

`cd` to the root directory and:

```
$ ./run_tests.py
```

## Design / components

### Approach

There are many ways to tackle this problem. It depends a lot on how this is going to be deployed, what are the resources, and what its usage is going to be like. One main restriction as indicated by the [exercise](EXERCISE.md) is that the input file may not fit in memory all at once. This affects how we read the file or maintain our internal structures. If we do not have enough memory to hold the file, we probably don't have enough memory to hold the anagram groups either.

For this reason, two approaches were followed.

1. We can only read one line each time from the input text file.
2. Since, we can not store all of the anagram groups in memory, we need an external storage. This could be a database, a NoSQL one works fine. For the purposes of this exercise, I went for the simple Python built-in persistent key/value pair storage, `shelve`. I've also tried `sqlite3` and `redis` in a Docker container, but I noticed they were performing worse when running the examples provided. Should we need to convert this code to be multi-threaded, this decision needs to be re-considered. `shelve` is not thread-safe but `redis` is. Using this storage and approach, we never hold more than one line or group.

**Note**

One reason I wanted to try `redis` is that `shelve` does not support append to a key, without extracting the whole value first. So, as mentioned in the [assumptions](#assumptions), potentially, if all of the lines of the input file are anagrams of the same group, we might not be able to load them all at once when inserting.

#### Algorithm

The general algorithm of finding the anagram groups, is:

```
For each word of the input file:
    Sort it alphabetically (key).
    Append the word to any already existing ones, under this key.

Return one-by-one the stored key/value pairs.
```

#### Abstraction

`AnagramFinder` class is responsible for taking the input file and finding the groups, according to the restrictions mentioned above. It is abstracted from what the exercise wants the output to look like, it only deals with sets of words, but a print function could easily be part of it.

#### Testing

Since this is quite I/O-heavy code, testing it can be challenging. My approach was to abstract as much as I think makes sense, and test those abstracted methods. This is more on the unit tests side, rather than integration tests; I wanted to avoid using a lot of mocking. I did add some sanity-check tests though for functions that use external resources (input file).

## Assumptions

1. We can always hold one line in memory. There will not be a big enough string in the text input file, we cannot handle.
2. We can always hold the anagram groups in memory.
3. CLI script is used correctly

## Areas for improvement

1. Error handling. The command line tool does not check for invalid/missing values
2. Logging. There isn't any explicit logging taking place. This includes feedback to standard output or showing/writing errors when they occur.

## Links

-   [Exercise](EXERCISE.md)
-   [shelve](https://docs.python.org/3/library/shelve.html)
