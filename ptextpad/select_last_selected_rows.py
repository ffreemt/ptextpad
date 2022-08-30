"""
Select last selected rows of two tuples.

For neualigner, actionSet_Row_Numbers.
"""
# import logging
# from nose.tools import (eq_, with_setup)

# LOGGER = logging.getLogger(__name__)
# LOGGER.addHandler(logging.NullHandler())
from logzero import logger


def select_last_selected_rows(lst) -> (int, int):
    """
    Select last rows of two tuples from a list.
    """
    if not isinstance(lst, list):
        logger.debug(" Input not a list, return None")
        return None
    lrow = -1
    rrow = -1
    for elm in lst:
        if elm[1] == 0:  # col0-> lrow
            lrow = elm[0]
        else:
            rrow = elm[0]
    return lrow, rrow


# @with_setup(my_setup)
def test_1():
    """test_[[0, 1], [2, 0], [4, 1], [5, 0]] +++."""
    lst = [[0, 1], [2, 0], [4, 1], [5, 0]]
    exp = (5, 4)
    out = select_last_selected_rows(lst)

    # eq_(exp, out)
    assert exp == out


# @with_setup(my_setup)
def test_2():
    """test_[[0, 1], [2, 1], [4, 1], [5, 1]] +++."""
    lst = [[0, 1], [2, 1], [4, 1], [5, 1]]
    exp = (-1, 5)
    out = select_last_selected_rows(lst)

    # eq_(exp, out)
    assert exp == out


# @with_setup(my_setup)
def test_3():
    """test_[[5, 1], [2, 1], [4, 1], [0, 1]] +++."""
    lst = [[5, 1], [2, 1], [4, 1], [0, 1]]
    exp = (-1, 0)
    out = select_last_selected_rows(lst)

    # eq_(exp, out)
    assert exp == out


# @with_setup(my_setup)
def test_4():
    """test_[[5, 0], [2, 0], [4, 0], [0, 0]] +++."""
    lst = [[5, 0], [2, 0], [4, 0], [0, 0]]
    exp = (0, -1)
    out = select_last_selected_rows(lst)

    # eq_(exp, out)
    assert exp == out
