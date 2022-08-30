"""Gen a set.

get_anchor_set(list0):
set_anchor: Set an anchor on an nx3 list.
"""
import logging

from .zip_longest_middle import zip_longest_middle

# from nose.tools import (eq_, with_setup)


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def get_anchor_set(list0):
    """Gen get_anchor_set."""
    try:
        colno = len(list0[0])
    except (NameError, IndexError) as exc:
        LOGGER.critical(" exc: %s ", exc)
        return None

    if colno < 3:
        LOGGER.warning(" merit col not available, exiting...")
        return None

    list1 = list0[:]
    anchor_set = []
    for (ith, elm) in enumerate(list1):
        try:
            merit0 = float(elm[2])
        except ValueError:  # as exc:
            # LOGGER.debug(' exc: %s ', exc)
            merit0 = -1.0
        if merit0 > 0:
            anchor_set += [ith]

    return anchor_set


def my_setup_function():
    """my_setup_function"""

    logging.basicConfig(
        format="%(name)s-ln:%(lineno)d:%(message)s:", level=logging.DEBUG
    )

    # LOGGER.debug(" LOGGER.debug in my_setup_function()")

    len1 = 20
    len2 = 15
    len2 = len1 + 1
    col1 = list(range(len1))
    col2 = list(range(len2))
    col12 = zip_longest_middle(col1, col2, fillvalue="")
    testarray = []

    for elm in col12:
        testarray.append([elm[0], elm[1], ""])
    assert len(testarray) == len1 if len1 > len2 else len2
    return testarray


def my_teardown_function():
    """my_teardown_function"""
    # LOGGER.debug(" LOGGER.debug in my_teardown_function()")
    pass


# @with_setup(my_setup_function, my_teardown_function)
def test_0():
    """test 0"""
    LOGGER.debug(" LOGGER.debug in test_0()")
    # testarray = my_setup_function()
    len1 = 20
    len2 = 15
    len2 = len1 + 1
    col1 = list(range(len1))
    col2 = list(range(len2))
    col12 = zip_longest_middle(col1, col2, fillvalue="")
    testarray = []

    for elm in col12:
        testarray.append([elm[0], elm[1], ""])

    lpos = 0
    expected = []
    testarray[lpos][2] = 1
    expected += [lpos]
    out = get_anchor_set(testarray)

    # eq_(expected, out)
    assert expected == out

    lpos = 10
    testarray[lpos][2] = 1
    expected += [lpos]
    out = get_anchor_set(testarray)

    # eq_(expected, out)
    assert expected == out

    lpos = 10
    testarray[lpos][2] = -1
    expected.remove(lpos)
    out = get_anchor_set(testarray)

    # eq_(expected, out)
    assert expected == out

    lpos = 10
    testarray[lpos][2] = "a"
    out = get_anchor_set(testarray)

    # eq_(expected, out)
    assert expected == out
