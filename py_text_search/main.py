from collections import defaultdict
from os import listdir
from os.path import isfile, join
from string import punctuation


class TextSearchException(Exception):
    pass


class InvalidFilePath(TextSearchException):
    pass


class UnableToProcessFile(TextSearchException):
    pass


class NoMatchesFound(TextSearchException):
    pass


class InvalidSearchTextPassed(TextSearchException):
    pass


def read_files(path_name):
    """
    Reads the list of file in the given path
    :param path_name: File path name
    :return: List of file present in the path
    """
    if not path_name:
        raise InvalidFilePath('Empty file path given')
    try:
        files_in_path = [
            join(path_name, f)
            for f in listdir(path_name)
            if isfile(join(path_name, f))
        ]
    except FileNotFoundError:
        raise InvalidFilePath(
            'Path {} not present in local machine. '
            'Please try different path'.format(
                path_name
            )
        )
    return [f for f in files_in_path if f.endswith('.txt')]


def build_index(files):
    """
    Builds the file word frequency map from the given files
    :param files: List of files
    :return: in-memory file and words frequency dictionary
    """
    file_word_frequency_map = {}
    for file_name in files:
        dictionary = defaultdict(int)
        try:
            file_generator = (row for row in open(file_name))
            for row in file_generator:
                for word in row.split():
                    dictionary[process_word(word)] += 1
            file_word_frequency_map[file_name] = dictionary
        except Exception as e:
            raise UnableToProcessFile(
                'Unable to process file: {0} Reason: {1}'.format(
                    file_name,
                    e,
                )
            )

    return file_word_frequency_map


def process_word(word):
    """
    Process word by applying transformation logic
    :param word: Input word to be transform
    :return: Transformed output
    """
    # Removing punctuations from the words
    new_word = word.translate(word.maketrans('', '', punctuation))
    # Ignoring the case
    new_word = new_word.lower()
    return new_word


def find_words(file_word_frequency_map, search_string):
    """
    Finds words and sends the results
    :param file_word_frequency_map: in-memory
        file and words frequency dictionary
    :param search_string: search string
    :return: unsorted Text search results dictionary
    """
    if not search_string:
        raise InvalidSearchTextPassed('Empty search text passed')
    search_string = search_string.lower()

    search_results = {}
    for file_name, dictionary in file_word_frequency_map.items():

        total_words = 0
        found_words = 0
        sum_of_occurrences = 0

        for word in search_string.split():
            total_words += 1

            if word in dictionary:
                found_words += 1
                sum_of_occurrences += dictionary[word]

        found_percentage = (found_words/total_words) * 100
        if found_percentage:
            # To rank results; Sum of occurrences
            #  is also used along with found %
            search_results[file_name] = (
                found_percentage,
                sum_of_occurrences
            )

    if not search_results:
        raise NoMatchesFound('no matches found')
    return search_results


def rank_results(search_results, display_only=10):
    """
    Sorts and Ranks the Search results
    :param search_results: unsorted Text search results dictionary
    :param display_only: Number of results to display
    :return: Sorted text search results list
    """
    sorted_file_names = sorted(search_results, reverse=True)
    result_ranks = []
    for file in sorted_file_names:
        result = TextSearchResult(
            file,
            search_results[file][0],
            search_results[file][1],
        )
        result_ranks.append(result)
    return result_ranks[:display_only]


class TextSearchResult:
    """
    Structure to hold fileName and scores
    """
    def __init__(self, file_name, score, occurrence):
        self.file_name = file_name
        self.score = score
        self.occurrence = occurrence

    def message(self):
        return '{0} | {1:.2f}% match | {2} occurrences'.format(
            self.file_name.split('/')[-1],
            self.score,
            self.occurrence,
        )
