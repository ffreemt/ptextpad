"""Do list_to_selected_rows.

Refer to continuous numbers set.txt in pyqt
"""
import logging
from itertools import groupby

# from nose.tools import eq_, with_setup

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def ranges(lst):
    """Find continuous indices"""
    sorted_lst = sorted(lst)
    pos = (j - i for i, j in enumerate(sorted_lst))
    t = 0
    for i, els in groupby(pos):
        l = len(list(els))
        el = sorted_lst[t]
        t += l
        yield range(el, el + l)


def list_to_selected_rows(lst, currindex):
    """Find continuous indices, given the current index.

    Generate a continuous set of rows for a list and a row number.

    The continuous set contains the given row or the last batch of rows in the list.

    :in:    indice list, currindex
    :out:   range(i,j)
    """
    if not isinstance(lst, list):
        LOGGER.warning(" Input not a list, return None.")
        return None

    if not lst:
        LOGGER.warning(" Input empty, return None.")
        return None

    elm = lst[-1]
    for elm in ranges(lst):
        if currindex in elm:
            break
    return elm


def my_setup():
    """my_setup."""

    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


# @with_setup(my_setup)
def test_():
    """test_+++."""
    lst = [2, 3, 4, 12, 13, 14, 15, 16, 17]
    lst = [5, 14, 2, 3, 4, 12, 15, 13, 16, 17]
    currindex = 3
    exp = range(2, 6)
    out = list_to_selected_rows(lst, currindex)

    # eq_(exp, out)
    assert exp == out

    currindex = 7
    exp = range(12, 18)
    out = list_to_selected_rows(lst, currindex)

    # eq_(exp, out)
    assert exp == out

    currindex = 17
    exp = range(12, 18)
    out = list_to_selected_rows(lst, currindex)

    # eq_(exp, out)
    assert exp == out

    currindex = 27
    exp = range(12, 18)
    out = list_to_selected_rows(lst, currindex)

    # eq_(exp, out)
    assert exp == out

    currindex = 1
    exp = range(12, 18)
    out = list_to_selected_rows(lst, currindex)

    # eq_(exp, out)
    assert exp == out
