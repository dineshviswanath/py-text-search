import os
import tempfile

import pytest

from py_text_search.main import (InvalidFilePath, NoMatchesFound, build_index,
                                 find_words, process_word, rank_results,
                                 read_files)

TEST_PATH = tempfile.gettempdir()
FILE_NAME = TEST_PATH+'/file1.txt'


class TestTextSearch:

    @pytest.fixture
    def create_file(self):
        self.create_tmp_file('file1.txt', 'to be or not to be')

    def create_tmp_file(self, name, content):
        full_path = os.path.join(tempfile.gettempdir(), name)
        with open(full_path, 'w') as f:
            f.writelines(content)
        return full_path

    def test_no_file_found(self):
        with pytest.raises(InvalidFilePath):
            read_files('SomeNotFoundRandomPath')

    def test_no_file_empty_path(self):
        with pytest.raises(InvalidFilePath):
            read_files(None)

    def test_file_found(self, create_file):
        files_to_process = read_files(TEST_PATH)
        assert len(files_to_process) != 0

    def test_build_index(self, create_file):
        files_to_process = read_files(TEST_PATH)
        file_word_frequency_map = build_index(files_to_process)
        assert len(file_word_frequency_map) != 0
        count = file_word_frequency_map[FILE_NAME]
        self.assert_file_content(count)

    @pytest.mark.parametrize("input_word, output_word", [
        ("a", "a"),
        ("a!", "a"),
        ("Hello", "hello"),
        ("hi_dear", "hidear"),
        ("IaMgRoOt", "iamgroot"),
        ("cloud9", "cloud9"),
    ])
    def test_process_word(self, input_word, output_word):
        assert process_word(input_word) == output_word

    def assert_file_content(self, count):
        assert count['to'] == 2
        assert count['be'] == 2
        assert count['or'] == 1
        assert count['not'] == 1

    def test_find_and_rank(self, create_file):
        files_to_process = read_files(TEST_PATH)
        file_word_frequency_map = build_index(files_to_process)

        ranks = find_words(
            file_word_frequency_map,
            'to be or not'
        )
        assert ranks[FILE_NAME] == (100, 6)

        ranks = find_words(
            file_word_frequency_map,
            'to be or Unknown'
        )
        assert ranks[FILE_NAME] == (75, 5)

        ranks = find_words(
            file_word_frequency_map,
            'to be NotFound Unknown'
        )
        assert ranks[FILE_NAME] == (50, 4)

        ranks = find_words(
            file_word_frequency_map,
            'to NotReally NotFound Unknown'
        )
        assert ranks[FILE_NAME] == (25, 2)

        with pytest.raises(NoMatchesFound):
            find_words(
                file_word_frequency_map,
                'Rover NotReally NotFound Unknown'
            )

    def test_get_top_3_ranks(self, create_file):
        self.create_tmp_file('file2.txt', 'to')
        self.create_tmp_file('file3.txt', 'be')
        self.create_tmp_file('file4.txt', 'or')

        files_to_process = read_files(TEST_PATH)
        file_word_frequency_map = build_index(files_to_process)

        search_results = find_words(file_word_frequency_map, 'to be or not')
        output_ranks = rank_results(search_results, 3)
        assert len(output_ranks) == 3
