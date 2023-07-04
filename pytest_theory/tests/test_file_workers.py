from my_funcs.file_workers import read_from_file


def test_read_file():
    test_data = ['one\n', 'two\n', 'three\n']
    assert test_data == read_from_file("data/testfile.txt")
