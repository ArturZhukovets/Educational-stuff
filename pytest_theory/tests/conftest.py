import pytest


def create_test_data(testdata: [list[str]]):
    if not isinstance(testdata, list):
        raise TypeError
    with open("data/testfile.txt", 'a') as file:
        file.writelines(testdata)


@pytest.fixture(autouse=True)  # `autouse` flag позволяет каждый раз запускать данную фикстуру
def clean_text_file():
    with open("data/testfile.txt", "w"):
        pass
    create_test_data(testdata=["one\n", "two\n", "three\n"])
