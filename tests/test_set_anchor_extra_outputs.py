"""Test."""
# pylint: disable=invalid-name
from itertools import zip_longest

from logzero import logger

# from nose.tools import eq_, with_setup
from ptextpad.get_anchor_set import get_anchor_set
from ptextpad.set_anchor import set_anchor
from ptextpad.set_anchor_extra_outputs import set_anchor_extra_outputs
from ptextpad.zip_longest_middle import zip_longest_middle

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


# @with_setup(my_setup_function, my_teardown_function)
def test_00():
    """Test_00 set_anchor_extra_outputs."""
    # logging.basicConfig(level=logging.DEBUG)

    logger.debug(" logger.debug in test_()")
    # testarray = my_setup_function()
    testarray = [list(elm) for elm in zip_longest(*zip(*col12), [""], fillvalue="")]

    lpos = 0
    rpos = 0
    out = set_anchor(testarray, lpos, rpos, merit=1)
    expected = testarray[:]
    expected[0][2] = 1

    # eq_(expected, out)
    assert expected == out

    logger.debug(" one more time ... ")
    meritvar = 0.5
    out = set_anchor(testarray, lpos, rpos, merit=meritvar)

    # eq_(expected, out)
    assert expected == out

    out1, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(
        testarray, lpos, rpos, merit=1
    )
    out1, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(
        testarray, lpos, rpos, merit=meritvar
    )
    # logger.debug(" out1: %s  at_row: %s row_numbers:%s rows_to_add %s", out1, at_row, row_numbers, rows_to_add)

    # eq_(out, out1)
    assert out == out1

    out2 = testarray[:]
    for ith in range(row_numbers):
        out2.pop(at_row)

    for ith, elm in enumerate(rows_to_add):
        out2.insert(at_row + ith, elm)

    logger.debug("out2: %s", out2)

    # eq_(out1, out2)
    assert out1 == out2


def test_35x():
    """Test_35x set_anchor_extra_outputs."""
    # import numpy as np

    # logging.basicConfig(level=logging.DEBUG)

    logger.debug(" logger.debug in test_()")
    # testarray = my_setup_function()
    testarray = [*zip_longest(*zip(*col12), [""], fillvalue="")]

    lpos = 3
    rpos = 5

    # testarray
    testarray = [*zip_longest(*zip(*col12), [""], fillvalue="")]
    out = set_anchor(testarray, lpos, rpos)

    expected = testarray[:]
    expected = [
        [0, 0, ""],
        [1, 1, ""],
        ["", 2, ""],
        ["", 3, ""],
        [2, 4, ""],
        [3, 5, 1],
        [4, 6, ""],
        [5, 7, ""],
        [6, 8, ""],
        [7, 9, ""],
        [8, 10, ""],
        [9, 11, ""],
        [10, 12, ""],
        [11, "", ""],
        [12, 13, ""],
        [13, 14, ""],
        [14, 15, ""],
        [15, 16, ""],
        [16, 17, ""],
        [17, 18, ""],
        [18, 19, ""],
        [19, 20, ""],
    ]

    # print(" %s \n\n %s \n\n * * * * * " % (expected, out))
    # print(" %s \n\n %s " % (np.array(expected), np.array(out)))

    # expected[0][2] = 1
    # eq_(expected, out)
    assert expected == out

    # ***************
    out1, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(
        testarray, lpos, rpos
    )
    logger.debug(
        " out1: %s  at_row: %s row_numbers:%s rows_to_add %s",
        out1,
        at_row,
        row_numbers,
        rows_to_add,
    )

    # eq_(out, out1)
    assert out == out1

    out2 = testarray[:]
    for ith in range(row_numbers):
        out2.pop(at_row)

    for ith, elm in enumerate(rows_to_add):
        out2.insert(at_row + ith, elm)

    logger.debug("out2: %s", out2)
    # eq_(out1, out2)
    assert out1 == out2


def test_35_1215():
    """Test_35_1215."""
    # import numpy as np

    # logging.basicConfig(level=logging.DEBUG)

    logger.debug(" logger.debug in test_35_1215()")
    testarray = [
        [0, 0, ""],
        [1, 1, ""],
        ["", 2, ""],
        ["", 3, ""],
        [2, 4, ""],
        [3, 5, 1],
        [4, 6, ""],
        [5, 7, ""],
        [6, 8, ""],
        [7, 9, ""],
        [8, 10, ""],
        [9, 11, ""],
        [10, 12, ""],
        [11, "", ""],
        [12, 13, ""],
        [13, 14, ""],
        [14, 15, ""],
        [15, 16, ""],
        [16, 17, ""],
        [17, 18, ""],
        [18, 19, ""],
        [19, 20, ""],
    ]

    # print(np.array(testarray))

    lpos = 12
    rpos = 15
    out = set_anchor(testarray, lpos, rpos)

    expected = [
        [0, 0, ""],
        [1, 1, ""],
        ["", 2, ""],
        ["", 3, ""],
        [2, 4, ""],
        [3, 5, 1],
        [4, 6, ""],
        [5, 7, ""],
        [6, 8, ""],
        ["", 9, ""],
        ["", 10, ""],
        [7, 11, ""],
        [8, 12, ""],
        [9, 13, ""],
        [10, 14, 1.0],
        [11, 15, ""],
        [12, 16, ""],
        [13, 17, ""],
        [14, "", ""],
        [15, "", ""],
        [16, "", ""],
        [17, 18, ""],
        [18, 19, ""],
        [19, 20, ""],
    ]

    # print(" %s \n\n %s \n * * * * * \n " % (expected, out))
    # print(" %s \n\n %s " % (np.array(expected), np.array(out)))

    # expected[0][2] = 1
    # eq_(expected, out)
    assert expected == out

    # ***************
    out1, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(
        testarray, lpos, rpos
    )
    logger.debug(
        "\ntest_35_1215\n out1: %s\n  at_row: %s\n row_numbers:%s\n rows_to_add %s\n",
        out1,
        at_row,
        row_numbers,
        rows_to_add,
    )

    # eq_(out, out1)
    assert out == out1

    out2 = testarray[:]
    for ith in range(row_numbers):
        out2.pop(at_row)

    for ith, elm in enumerate(rows_to_add):
        out2.insert(at_row + ith, elm)

    logger.debug("out2: %s", out2)

    # eq_(out1, out2)
    assert out1 == out2


def test_final1():
    """Test_35 1215 finall."""
    # import numpy as np

    # logging.basicConfig(level=logging.DEBUG)

    logger.debug(" logger.debug in test_3535()")
    testarray = [
        [0, 0, ""],
        [1, 1, ""],
        ["", 2, ""],
        ["", 3, ""],
        [2, 4, ""],
        [3, 5, 1],
        [4, 6, ""],
        [5, 7, ""],
        [6, 8, ""],
        ["", 9, ""],
        ["", 10, ""],
        [7, 11, ""],
        [8, 12, ""],
        [9, 13, ""],
        [10, 14, 1.0],
        [11, 15, ""],
        [12, 16, ""],
        [13, 17, ""],
        [14, "", ""],
        [15, "", ""],
        [16, "", ""],
        [17, 18, ""],
        [18, 19, ""],
        [19, 20, ""],
    ]

    # print(np.array(testarray))

    lpos = 1
    rpos = 3
    out = set_anchor(testarray, lpos, rpos)

    expected = [
        [0, 0, ""],
        ["", 1, ""],
        ["", 2, ""],
        [1, 3, 1.0],
        [2, 4, ""],
        [3, 5, 1],
        [4, 6, ""],
        [5, 7, ""],
        [6, 8, ""],
        ["", 9, ""],
        ["", 10, ""],
        [7, 11, ""],
        [8, 12, ""],
        [9, 13, ""],
        [10, 14, 1.0],
        [11, 15, ""],
        [12, 16, ""],
        [13, 17, ""],
        [14, "", ""],
        [15, "", ""],
        [16, "", ""],
        [17, 18, ""],
        [18, 19, ""],
        [19, 20, ""],
    ]

    # print(" %s \n\n %s \n * * * * * \n " % (expected, out))
    # print(" %s \n\n %s " % (np.array(expected), np.array(out)))

    # expected[0][2] = 1
    assert expected == out

    # ***************
    out1, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(
        testarray, lpos, rpos
    )
    logger.debug(
        " out1: %s\n  at_row: %s\n row_numbers:%s\n rows_to_add %s",
        out1,
        at_row,
        row_numbers,
        rows_to_add,
    )

    assert out == out1
    out2 = testarray[:]
    for ith in range(row_numbers):
        out2.pop(at_row)

    for ith, elm in enumerate(rows_to_add):
        out2.insert(at_row + ith, elm)

    logger.debug("out2: %s", out2)
    # eq_(out1, out2)
    assert out1 == out2


def test_final2():
    """Test_35 1215 final2."""
    # import numpy as np

    # logging.basicConfig(level=logging.DEBUG)

    logger.debug(" logger.debug in test_3535()")
    testarray = [
        [0, 0, ""],
        ["", 1, ""],
        ["", 2, ""],
        [1, 3, 1.0],
        [2, 4, ""],
        [3, 5, 1],
        [4, 6, ""],
        [5, 7, ""],
        [6, 8, ""],
        ["", 9, ""],
        ["", 10, ""],
        [7, 11, ""],
        [8, 12, ""],
        [9, 13, ""],
        [10, 14, 1.0],
        [11, 15, ""],
        [12, 16, ""],
        [13, 17, ""],
        [14, "", ""],
        [15, "", ""],
        [16, "", ""],
        [17, 18, ""],
        [18, 19, ""],
        [19, 20, ""],
    ]

    # print(np.array(testarray))

    lpos = 1
    rpos = 3
    out = set_anchor(testarray, lpos, rpos)

    expected = [
        [0, 0, ""],
        ["", 1, ""],
        ["", 2, ""],
        [1, 3, 1.0],
        [2, 4, ""],
        [3, 5, 1],
        [4, 6, ""],
        [5, 7, ""],
        [6, 8, ""],
        ["", 9, ""],
        ["", 10, ""],
        [7, 11, ""],
        [8, 12, ""],
        [9, 13, ""],
        [10, 14, 1.0],
        [11, 15, ""],
        [12, 16, ""],
        [13, 17, ""],
        [14, "", ""],
        [15, "", ""],
        [16, "", ""],
        [17, 18, ""],
        [18, 19, ""],
        [19, 20, ""],
    ]

    # print(" %s \n\n %s \n * * * * * \n " % (expected, out))
    # print(" %s \n\n %s " % (np.array(expected), np.array(out)))

    # expected[0][2] = 1
    # eq_(expected, out)
    assert expected == out

    # ***************
    out1, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(
        testarray, lpos, rpos
    )
    logger.debug(
        " out1: %s\n  at_row: %s\n row_numbers:%s\n rows_to_add %s",
        out1,
        at_row,
        row_numbers,
        rows_to_add,
    )

    # eq_(out, out1)
    assert out == out1

    out2 = testarray[:]
    for ith in range(row_numbers):
        out2.pop(at_row)

    for ith, elm in enumerate(rows_to_add):
        out2.insert(at_row + ith, elm)

    logger.debug("out2: %s", out2)
    # eq_(out1, out2)
    assert out1 == out2


def test_final3():
    """Test_35 1215 final3."""
    # import numpy as np

    # logging.basicConfig(level=logging.DEBUG)

    logger.debug(" logger.debug in test_3535()")
    testarray = [
        [0, 0, ""],
        ["", 1, ""],
        ["", 2, ""],
        [1, 3, 1.0],
        [2, 4, ""],
        [3, 5, 1],
        [4, 6, ""],
        [5, 7, ""],
        [6, 8, ""],
        ["", 9, ""],
        ["", 10, ""],
        [7, 11, ""],
        [8, 12, ""],
        [9, 13, ""],
        [10, 14, 1.0],
        [11, 15, ""],
        [12, 16, ""],
        [13, 17, ""],
        [14, "", ""],
        [15, "", ""],
        [16, "", ""],
        [17, 18, ""],
        [18, 19, ""],
        [19, 20, ""],
    ]

    # print(np.array(testarray))

    lpos = 6
    rpos = 10
    out = set_anchor(testarray, lpos, rpos)
    out = set_anchor(testarray, lpos, rpos, merit=1)
    out = set_anchor(testarray, lpos, rpos, merit=1)

    expected = [
        [0, 0, ""],
        ["", 1, ""],
        ["", 2, ""],
        [1, 3, 1.0],
        [2, 4, ""],
        [3, 5, 1],
        ["", 6, ""],
        ["", 7, ""],
        ["", 8, ""],
        ["", 9, ""],
        [4, 10, 1.0],
        [5, 11, ""],
        [6, "", ""],
        [7, "", ""],
        [8, 12, ""],
        [9, 13, ""],
        [10, 14, 1.0],
        [11, 15, ""],
        [12, 16, ""],
        [13, 17, ""],
        [14, "", ""],
        [15, "", ""],
        [16, "", ""],
        [17, 18, ""],
        [18, 19, ""],
        [19, 20, ""],
    ]

    # print(" %s \n\n %s \n * * * * * \n " % (expected, out))
    # print(" %s \n\n %s " % (np.array(expected), np.array(out)))

    # expected[0][2] = 1
    # eq_(expected, out)
    assert expected == out

    # ***************
    # out1, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(testarray, lpos, rpos)
    out1, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(
        testarray, lpos, rpos, merit=1
    )
    out1, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(
        testarray, lpos, rpos, merit=1
    )
    logger.debug(
        " out1: %s\n  at_row: %s\n row_numbers:%s\n rows_to_add %s",
        out1,
        at_row,
        row_numbers,
        rows_to_add,
    )

    # eq_(out, out1)
    assert out == out1

    out2 = testarray[:]
    for ith in range(row_numbers):
        out2.pop(at_row)

    for ith, elm in enumerate(rows_to_add):
        out2.insert(at_row + ith, elm)

    logger.debug("out2: %s", out2)
    # eq_(out1, out2)
    assert out1 == out2


# @with_setup(my_setup_function, my_teardown_function)
def test_getanchorset():
    """Test get_anchor_set."""
    # testarray = my_setup_function()

    testarray = [list(elm) for elm in zip_longest(*zip(*col12), [""], fillvalue="")]

    anchor_set = get_anchor_set(testarray)
    # eq_(anchor_set, [])
    assert anchor_set == []

    testarray[0][2] = 1
    anchor_set = get_anchor_set(testarray)
    # eq_(anchor_set, [0])
    assert anchor_set == [0]

    testarray[10][2] = 0.5
    anchor_set = get_anchor_set(testarray)
    # eq_(anchor_set, [0, 10])
    assert anchor_set == [0, 10]

    testarray[10][2] = "a"
    anchor_set = get_anchor_set(testarray)
    # eq_(anchor_set, [0])
    assert anchor_set == [0]
