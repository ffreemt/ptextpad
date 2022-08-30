"""Update a list (for arraydata in tablemodel).

given: list0, irow, row_numbers, rows_to_add
out: updated list1

better use class?

# neualigner.py
to be adopted: based on (list0, irow=0, row_numbers=0, rows_to_add=[])

MyTableModel in mytablenb.py
# self.tableView_2.tablemodel = MyTable(self.tab_2, [['', '', '']]) # in neualigner.ui0.py
update_mytable(tableView_2.tablemodel, irow=0, row_numbers=0, rows_to_add=[])?

    tableView_2.tablemodel.layoutAboutToBeChanged.emit()
    for ith in range(row_numbers):
        tableView_2.tablemodle.arraydata.pop(at_row)

    for ith, elm in enumerate(rows_to_add):
        tableView_2.tablemodle.arraydata.insert(at_row + ith, elm)
    tableView_2.tablemodel.layoutChanged.emit()
"""

import logging
from copy import deepcopy

from nose.tools import eq_, with_setup

# from PyQt4.QtCore import *
# from PyQt4.QtGui import *


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def update_list(list0, irow=0, row_numbers=0, rows_to_add=[]):
    """
    Updates a list.

    given: list0, irow, row_numbers, rows_to_add
    out: updated list1

    for TableViw's data model update
    # neualigner.pyw
        self.tableView_2.tablemodel.layoutAboutToBeChanged.emit()
        for ith in range(row_numbers):
            self.tableView_2.myarray.pop(at_row)

        for ith, elm in enumerate(rows_to_add):
            self.tableView_2.myarray.insert(at_row + ith, elm)
        self.tableView_2.tablemodel.layoutChanged.emit()

    """

    # substitue list0 with tableView_2.tablemodel.arraydata in
    # def update_mytable(tableView_2, irow=0, row_numbers=0, rows_to_add=[])
    # tableView_2.tablemodel.layoutAboutToBeChanged.emit()
    # substitue list1 w with tableView_2.tablemodel.arraydata
    # noneed to return or return None

    # list1 = deepcopy(list0)  : change list0 in the following to list1

    # inplace update, make no copy of list0
    if row_numbers:
        if row_numbers > len(list0) - irow:
            row_numbers = len(list0) - irow
        for elm in range(row_numbers):
            list0.pop(irow)
    # insert after irow
    for (ith, elm) in enumerate(rows_to_add):
        list0.insert(irow + ith, elm)

    # tableView_2.tablemodel.layoutChanged.emit()

    return list0


def update_mytable(tablemodel, irow=0, row_numbers=0, rows_to_add=[]):
    """
    Updates data and model in tableView_2 by using update_list(tabelmode.arraydata, irow=0, row_numbers=0, rows_to_add=[])

    (for splitcell, mergcellup movecelldown ,mergecellup, mergecelldown)
    """
    tablemodel.layoutAboutToBeChanged.emit()
    LOGGER.debug("\n*update_mytable* arraydata[:6] %s ", tablemodel.arraydata[:6])
    # update_list(tablemodel.arraydata, irow=irow, row_numbers=row_numbers, rows_to_add=rows_to_add)
    tablemodel.arraydata = update_list(
        tablemodel.arraydata,
        irow=irow,
        row_numbers=row_numbers,
        rows_to_add=rows_to_add,
    )

    LOGGER.debug("  updated arraydata[:6] %s \n", tablemodel.arraydata[:6])

    tablemodel.layoutChanged.emit()


def my_setup(case=None):
    # case = 1
    rowlen = 5
    collen = 3

    if case is None:
        list0 = [[1, 2], [3, 4]]
    else:
        list0 = []
        for elm in range(rowlen):
            list0 += [[elm] * collen]

    # irow = 0
    # row_numbers = 1
    # rows_to_add = [[1, 2]]

    return list0


def gen_rows(rowlen=3, collen=3):
    """Gen rowlen rows of [0, collen]-."""
    # rowlen = 5
    # collen = 3

    list0 = []
    for elm in range(rowlen):
        list0 += [list(range(collen))]

    # irow = 0
    # row_numbers = 1
    # rows_to_add = [[1, 2]]

    return list0


def my_teardown():
    pass


@with_setup(my_setup, my_teardown)
def test_delete_more():
    """Test _delete_more."""

    list0 = my_setup()

    row_numbers = 3
    irow = 0
    rows_to_add = []

    expected = []
    out = update_list(list0, irow, row_numbers=row_numbers, rows_to_add=rows_to_add)

    eq_(expected, out)


@with_setup(my_setup, my_teardown)
def test_addonly():
    """Test 1: add only."""
    list0 = my_setup()

    row_numbers = 0
    irow = 3  # no delete if row_numbers = 0

    rows_to_add = [[4, 5]]
    expected = deepcopy(list0)
    expected.append([4, 5])
    # expected = expected[:irow] + [[4, 5]] + expected[irow:]

    out = update_list(list0, irow, row_numbers=row_numbers, rows_to_add=rows_to_add)

    eq_(expected, out)

    # =============
    list0 = my_setup()
    row_numbers = 0
    irow = 1  # no delete if row_numbers = 0

    rows_to_add = [[4, 5]]
    expected = deepcopy(list0)
    expected = expected[:irow] + [[4, 5]] + expected[irow:]

    out = update_list(list0, irow, row_numbers=row_numbers, rows_to_add=rows_to_add)

    eq_(expected, out)

    # =============
    list0 = my_setup()
    row_numbers = 0
    irow = 3  # no delete if row_numbers = 0

    rows_to_add = [[4, 5], [6, 7]]
    expected = deepcopy(list0)
    expected = expected[:irow] + rows_to_add + expected[irow:]

    out = update_list(list0, irow, row_numbers=row_numbers, rows_to_add=rows_to_add)

    eq_(expected, out)


def test_delete_irow3_n_add():
    """Test _delete_irow3_n_add."""
    # =============
    list0 = my_setup()
    row_numbers = 1
    irow = 3  # no delete if row_numbers = 0, irow len(list0)-1

    rows_to_add = [[4, 5], [6, 7]]
    expected = deepcopy(list0)
    expected = expected[:irow] + rows_to_add + expected[irow:]

    out = update_list(list0, irow, row_numbers=row_numbers, rows_to_add=rows_to_add)

    eq_(expected, out)


def test_delete_irow1_n_add():
    """Test _delete_irow1_n_add."""
    # =============
    list0 = my_setup()
    row_numbers = 1
    irow = 1  # no delete if row_numbers = 0, irow len(list0)-1

    rows_to_add = [[4, 5], [6, 7]]
    expected = [[1, 2], [4, 5], [6, 7]]
    # expected = expected[:irow] + rows_to_add + expected[irow:]

    out = update_list(list0, irow, row_numbers=row_numbers, rows_to_add=rows_to_add)

    eq_(expected, out)


@with_setup(my_setup, my_teardown)
def test_op_check():
    """Test _op_check."""
    list0 = my_setup(case=1)
    print("\n list0: %s" % list0)

    irow = 1
    print(" irow %s" % irow)

    row_numbers = 3
    print(" row_numbers %s " % row_numbers)

    rows_to_add = [[1, 2, 3]]
    rows_to_add = gen_rows(4, 2)

    print(" rows_to_add %s " % rows_to_add)

    len0 = len(list0)
    expected = my_setup(case=1)
    if irow <= 0:
        irow = 0
    if irow >= len0:
        irow = len0
    if (
        row_numbers >= len0 - irow
    ):  # irow + row_numbers >= len0 => row_numbers = len0 - irow
        row_numbers = len0 - irow

    expected = expected[:irow] + rows_to_add + expected[irow + row_numbers : len0]

    # with deepcopy
    # out = update_list(list0, irow, row_numbers, rows_to_add)
    # print('***\n', expected, '\n***\n', out)
    # eq_(expected, out)

    # update in place
    update_list(list0, irow, row_numbers, rows_to_add)
    print("***\n", expected, "\n***\n", list0)
    eq_(expected, list0)
