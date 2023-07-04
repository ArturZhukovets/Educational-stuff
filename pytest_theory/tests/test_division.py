import pytest

from my_funcs.utils import division

########################################################################################

def test_division_simple():
    assert division(15, 3) == 5

########################################################################################

@pytest.mark.parametrize(
    "a, b, expected_res",
    [(3, 1, 3), (10, 2, 5), (20, 10, 2), (20, 2, 10), (5, 2, 2.5)]
)
def test_division_parametrise(a: int, b: int, expected_res: int | float):
    assert division(a, b) == expected_res

########################################################################################

@pytest.mark.parametrize(
    "a, b, expected_exception",
    [(5, 0, ZeroDivisionError), (5, "string", TypeError)]
)
def test_division_exceptions(a: int, b: int, expected_exception):
    with pytest.raises(expected_exception):
        division(a, b)
