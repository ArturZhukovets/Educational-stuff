# import pytest
#
# @pytest.fixture(scope="session")
# def session_fixture():
#     print("Start session fixture")
#     yield 1
#     print("End session fixture")
#
#
# def test_1(session_fixture):
#     print("Start first test")
#     assert True
#
# def test_2(session_fixture):
#     num = session_fixture
#     print(f"Start second test, session fixture value is - {num}")
#     assert True
#
