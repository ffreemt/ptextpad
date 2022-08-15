"""Converts csv/txt using panda.read_csv.

csv_to_list
"""
import logging
import os
from itertools import zip_longest

import chardet
import pandas as pd

# from nose.tools import eq_, with_setup

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def csv_to_list(filepath):
    """Converts csv/txt using panda.read_csv.

    in: filepath
        pd.read_csv
        pd.read_table
    out: a list of 3 tuples for neualigner

    use pandas.read_csv, pandas.read_table
    """
    if not os.path.exists(filepath):
        LOGGER.warning(" %s does not exist, return None.", filepath)
        return None

    encoding = chardet.detect(open(filepath, "rb").read())["encoding"]
    try:
        df = pd.read_csv(filepath, header=None, encoding=encoding)
        # df = pd.read_csv(filepath, header=None, skip_blank_lines=True)
        LOGGER.info(" Successfully loaded.")
    except Exception as exc:
        LOGGER.error("Loading %s as csv file, failed: %s", filepath, exc)
        try:
            LOGGER.info("Tryint to load as tab (pd.read_table)")
            df = pd.read_table(filepath, header=None, encoding=encoding)
            LOGGER.info(" Successfully loaded.")
            # df = pd.read_table(filepath, header=None, skip_blank_lines=True)  # error_bad_lines=False,
        except Exception as exc:
            LOGGER.error("Loading %s as tab file, faied: %s", filepath, exc)

            LOGGER.warning(" return None")
            return None
    # replace NaN with ''
    df.fillna("", inplace=True)

    if len(df.iloc[0]) <= 1:
        # try one more time with table
        LOGGER.info("Loading as tab (pd.read_table)")
        df = pd.read_table(filepath, header=None, encoding=encoding)

        if len(df.iloc[0]) <= 1:
            LOGGER.warning(
                " The resultant dataframe has too few columns (<2), return None"
            )
            return None

    # if len(df) == 2:
    if len(df.iloc[0]) == 2:
        list0 = zip_longest(df[0], df[1], [""], fillvalue="")
    else:
        list0 = zip_longest(df[0], df[1], df[2])

    # convert to list
    list0 = [list(elm) for elm in list0]

    # remove rows with '' only
    list0 = [elm for elm in list0 if "".join(str(elm)).strip()]
    return list0


def my_setup():
    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


# nosetests -v --nologcapture
# @with_setup(my_setup)
def test_loadfileerror():
    """Test _loafileerror"""
    filepath = "abc"
    out = csv_to_list(filepath)
    assert out is None


# @with_setup(my_setup)
def test_notvalidnormalfile():
    """Test _notvalidnormalfile"""
    # filepath = r"D:\dl\Dropbox\mat-dir\python-my-codes-mat\csv_to_list.py"
    filepath = "ptextpad/csv_to_list.py"
    out = csv_to_list(filepath)
    assert out is None


# @with_setup(my_setup)
def test_Folding_Beijing_12Folding_Beijing_12():
    """Test _Folding_Beijing_12Folding_Beijing_12."""
    filepath = r"D:\dl\Dropbox\shuangyu_ku\txt-books\aligned\Folding_Beijing_12.txt"
    filepath = "data/Folding_Beijing_12.txt"
    list0 = csv_to_list(filepath)

    exp1 = 1112  # len
    exp2 = ["Folding Beijing", "北京折叠", ""]  # list0[0]
    exp3 = ["It was time to go to work.", "他看看时间，该去上班了。", ""]  # last

    if list0:
        assert exp1 == len(list0)
    assert exp2 == list0[0]
    assert exp3 == list0[-1]


# @with_setup(my_setup)
def test_Folding_Folding_Beijing_12xls():
    """Test _Folding_Beijing_12xls."""
    filepath = r"D:\dl\Dropbox\shuangyu_ku\txt-books\aligned\Folding_Beijing_12xls.txt"
    filepath = "data/Folding_Beijing_12xls.txt"
    list0 = csv_to_list(filepath)

    exp1 = 1112  # len
    exp2 = ["Folding Beijing", "北京折叠", ""]  # list0[0]
    exp3 = ["It was time to go to work.", "他看看时间，该去上班了。", ""]  # last

    assert exp1 == len(list0)
    assert exp2 == list0[0]
    assert exp3 == list0[-1]
