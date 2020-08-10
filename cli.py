import sys

from py_text_search.main import (InvalidFilePath, InvalidSearchTextPassed,
                                 NoMatchesFound, UnableToProcessFile,
                                 build_index, find_words, rank_results,
                                 read_files)

if len(sys.argv) != 2:
    print('Error: Invalid Syntax')
    print('Usage: python cli.py <pathToDirectoryContainingTextFiles>')
    sys.exit(1)

path = sys.argv[1]
try:
    files = read_files(path)
    file_word_frequency_map = build_index(files)
    print('{} files read in the directory'.format(len(file_word_frequency_map)))
except (InvalidFilePath, UnableToProcessFile) as e:
    print(e)
    sys.exit(1)

while True:
    print('Search> ', end='')
    try:
        search_text = input()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(1)

    if search_text == ':quit':
        print('bye!')
        break
    try:
        search_results = find_words(file_word_frequency_map, search_text)
    except (InvalidSearchTextPassed, NoMatchesFound) as e:
        print(e)
    else:
        results = rank_results(search_results)
        for res in results:
            print(res.message())