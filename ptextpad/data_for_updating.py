# coding: utf-8
"""
Funcitons for gen various ops.

"""
import logging
import re
from itertools import zip_longest

from .update_list import update_list

# from nose.tools import (eq_, with_setup)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

splittag_ = "|||"
splittag_ = re.compile(r"\|{3,}")

# from update_list import update_list


def data_for_split0(list0, idxi, idxj, splittag=splittag_):
    """
    data_for_split0.
    """
    # tmpstr = str(list0[idxi][idxj]).split(splittag, 1)

    # amended 2022 06 27
    tmpstr = re.split(splittag, str(list0[idxi][idxj]), 1)

    row_numbers = 1

    urow = list0[idxi][:]
    urow[idxj] = tmpstr[0]

    if len(tmpstr) == 1:
        rows_to_add = [urow]
    elif len(tmpstr) == 2:
        # lrow = list0[idxi][:]  # wrong
        lrow = [""] * len(urow)
        lrow[idxj] = tmpstr[1]
        rows_to_add = [urow, lrow]
    return idxi, row_numbers, rows_to_add


def data_for_splitdouble(vec0, splittag=splittag_):
    r"""Prep data_for_splitdouble.

    in: vec0, vec1, splittag='|||' or re.compile(r"\|{3,}")
    out: rows_to_add ([], or [urow, lrow])
    """

    # tmpstr0 = str(vec0[0]).split(splittag, 1)
    # tmpstr1 = str(vec0[1]).split(splittag, 1)

    # amended 2022 06 27
    tmpstr0 = re.split(splittag, str(vec0[0]), 1)
    tmpstr1 = re.split(splittag, str(vec0[1]), 1)

    # len(rows_to_add) limited to 1 or 2
    rows_to_add = [list(elm) for elm in zip_longest(tmpstr0, tmpstr1, fillvalue="")]

    rows_to_add[0] += [vec0[2]]  # attach merit
    if len(rows_to_add) == 2:
        rows_to_add[1] += [""]  # attach merit

    return rows_to_add

    # possible TODO need to find a way to select a cell or
    # may need to work this out
    # tmpstr0 = str(vec0[0]).split(splittag)
    # tmpstr1 = str(vec0[1]).split(splittag)

    # len(tmplist) any >=1
    # tmplist = [list(elm) for elm in zip_longest(tmpstr0, tmpstr1, fillvalue='')]

    # lrow = tmpist[-1] + ['']  # last row
    # urow = ?  # TODO
    # rows_to_add = [urow, lrow]


def data_for_split(vec0, idxj, splittag=splittag_):
    """
    data_for_split.
    """
    # tmpstr = str(vec0[idxj]).split(splittag, 1)

    # amended 2022 06 27
    tmpstr = re.split(splittag, str(vec0[idxj]), 1)

    urow = vec0[:]
    urow[idxj] = tmpstr[0]

    if len(tmpstr) == 1:
        rows_to_add = [urow]
    elif len(tmpstr) == 2:
        lrow = [""] * len(urow)
        lrow[idxj] = tmpstr[1]
        rows_to_add = [urow, lrow]
    return rows_to_add


def data_for_moveup(vec0, idxj):
    """Prep data_for_moveup."""
    lrow = vec0[:]
    lrow[idxj] = ""
    lrow[2] = ""

    urow = [""] * len(vec0)
    urow[idxj] = vec0[idxj]
    rows_to_add = [urow, lrow]

    return rows_to_add


def data_for_movedown(vec0, idxj):
    """Prep data_for_movedown."""
    urow = vec0[:]
    urow[idxj] = ""
    urow[2] = ""

    lrow = [""] * len(vec0)
    lrow[idxj] = vec0[idxj]
    rows_to_add = [urow, lrow]

    return rows_to_add


def data_for_mergedown(vec0, vec1, idxj, sep=" "):
    """Prep data_for_mergedown."""
    urow = vec0[:]
    lrow = vec1[:]

    urow[idxj] = ""
    lrow[idxj] = str(vec0[idxj]) + sep + str(vec1[idxj])

    urow[2] = ""
    lrow[2] = ""

    rows_to_add = [urow, lrow]

    return rows_to_add


def data_for_mergeup(vec0, vec1, idxj, sep=" "):
    """Prep data_for_mergeup."""
    urow = vec0[:]
    lrow = vec1[:]

    urow[idxj] = str(vec0[idxj]) + sep + str(vec1[idxj])
    lrow[idxj] = ""

    urow[2] = ""
    lrow[2] = ""

    rows_to_add = [urow, lrow]

    return rows_to_add


def my_setup():
    """my_setup"""
    logging.basicConfig(level=logging.DEBUG)


def gen_rows(rowlen=3, collen=3):
    """Gen rowlen rows of [0, collen]."""
    # rowlen = 5
    # collen = 3

    list0 = []
    for elm in range(rowlen):
        list0 += [list(range(collen))]

    # irow = 0
    # row_numbers = 1
    # rows_to_add = [[1, 2]]

    return list0


def test_gen_rows():
    """Test _gen_rows"""
    # !note the double brackets: [[]]
    assert [[0 == 1, 2]], gen_rows(1, 3)


# @with_setup(my_setup)
def test_data_for_split0():
    """Test _data_for_split0 old version for list."""
    list0 = gen_rows(3, 3)
    idxi = 1
    idxj = 1
    # list0[idxi][idxj] = 'abc i_neu_i xyz'
    list0[idxi][idxj] = "abc ||| xyz"
    print(" list0 %s " % list0)

    expected = (1, 1, [[0, "abc ", 2], ["", " xyz", ""]])
    print(" expected: %s %s %s" % expected)

    out = data_for_split0(list0, idxi, idxj)
    # print(" out: %s " % out)

    LOGGER.debug("out: %s", out)

    out1 = update_list(list0, out[0], out[1], out[2])
    LOGGER.debug(" updated list0 output: %s ", out1)
    LOGGER.debug(" updated list0 %s ", list0)

    assert expected == out


# @with_setup(my_setup)
def test_data_for_split():

    """
    test_data_for_split
    """

    vec0 = gen_rows(1, 3)[0]

    idxj = 1
    # list0[idxi][idxj] = 'abc i_neu_i xyz'
    vec0[idxj] = "abc ||| xyz"
    LOGGER.debug(" vec0 %s ", vec0)

    expected = [[0, "abc ", 2], ["", " xyz", ""]]
    LOGGER.debug(" expected: %s ", expected)

    out = data_for_split(vec0, idxj)
    # print(" out: %s " % out)

    LOGGER.debug("out: %s", out)

    assert expected == out


# @with_setup(my_setup)
def test_data_for_moveup():

    """
    test_data_for_moveup
    """

    vec0 = gen_rows(1, 3)[0]

    idxj = 1
    # list0[idxi][idxj] = 'abc i_neu_i xyz'

    expected = [["", 1, ""], [0, "", ""]]
    LOGGER.debug(" expected: %s ", expected)

    out = data_for_moveup(vec0, idxj)
    # print(" out: %s " % out)

    LOGGER.debug("out: %s", out)

    assert expected == out


# @with_setup(my_setup)
def test_data_for_movedown():

    """
    test_data_for_movedown
    """

    vec0 = gen_rows(1, 3)[0]

    idxj = 1
    # list0[idxi][idxj] = 'abc i_neu_i xyz'

    expected = [[0, "", ""], ["", 1, ""]]
    LOGGER.debug(" expected: %s ", expected)

    out = data_for_movedown(vec0, idxj)
    # print(" out: %s " % out)

    LOGGER.debug("out: %s", out)

    assert expected == out


# @with_setup(my_setup)
def test_data_for_mergedown():

    """
    test_data_for_mergedown
    """

    vec = gen_rows(2, 3)
    vec0 = vec[0]
    vec1 = vec[1]

    idxj = 1
    # list0[idxi][idxj] = 'abc i_neu_i xyz'

    expected1 = [[0, "", ""], [0, "1 1", ""]]
    LOGGER.debug(" expected: %s ", expected1)

    out1 = data_for_mergedown(vec0, vec1, idxj, " ")

    LOGGER.debug("out1: %s", out1)

    assert expected1 == out1

    expected2 = [[0, "", ""], [0, "11", ""]]
    LOGGER.debug(" expected: %s ", expected2)

    out2 = data_for_mergedown(vec0, vec1, idxj, "")
    # print(" out: %s " % out)

    LOGGER.debug("out2: %s", out2)

    assert expected2 == out2


# @with_setup(my_setup)
def test_data_for_mergeup():

    """
    test_data_for_mergeup
    """

    vec = gen_rows(2, 3)
    vec0 = vec[0]
    vec1 = vec[1]

    idxj = 1
    # list0[idxi][idxj] = 'abc i_neu_i xyz'

    expected1 = [[0, "1 1", ""], [0, "", ""]]
    LOGGER.debug(" expected: %s ", expected1)

    out1 = data_for_mergeup(vec0, vec1, idxj)
    # print(" out: %s " % out)

    LOGGER.debug("out: %s", out1)

    assert expected1 == out1

    expected2 = [[0, "11", ""], [0, "", ""]]
    LOGGER.debug(" expected: %s ", expected2)

    out2 = data_for_mergeup(vec0, vec1, idxj, "")
    # print(" out: %s " % out)

    LOGGER.debug("out: %s", out2)

    assert expected2 == out2


# @with_setup(my_setup)
def test_data_for_splitdouble():

    """
    test_data_for_splitdouble
    """

    vec0 = gen_rows(1, 3)[0]

    idxj = 1
    # list0[idxi][idxj] = 'abc i_neu_i xyz'
    vec0[idxj] = "abc ||| xyz"
    LOGGER.debug(" vec0 %s ", vec0)

    expected = [["0", "abc ", 2], ["", " xyz", ""]]
    LOGGER.debug(" expected: %s ", expected)

    out = data_for_splitdouble(vec0)
    # print(" out: %s " % out)

    LOGGER.debug("out: %s", out)

    assert expected == out

    vec0 = gen_rows(1, 3)[0]

    idxj = 0
    # list0[idxi][idxj] = 'abc i_neu_i xyz'
    vec0[idxj] = "abc ||| xyz"
    LOGGER.debug(" vec0 %s ", vec0)

    # expected = ([[0, 'abc ', 2], ['', ' xyz', '']])
    expected = [["abc ", "1", 2], [" xyz", "", ""]]
    LOGGER.debug(" expected: %s ", expected)

    out = data_for_splitdouble(vec0)
    # print(" out: %s " % out)

    LOGGER.debug("out: %s", out)

    assert expected == out

    vec0 = ["abc ||| xyz", "x|||y|||", 2]
    LOGGER.debug(" vec0 %s ", vec0)

    expected = [["abc ", "x", 2], [" xyz", "y|||", ""]]
    LOGGER.debug(" expected: %s ", expected)

    out = data_for_splitdouble(vec0)
    # print(" out: %s " % out)

    LOGGER.debug("out: %s", out)

    assert expected == out
