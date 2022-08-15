"""Obtain the trunk two files based on ofiles_2files."""
import os
from pathlib import Path

# from nose.tools import eq_
from .ofiles_2files import ofiles_2files


def twofiles_trunk(file1, file2=None, check=False):
    out, dummy2, dummy3 = ofiles_2files(file1, file2, check=check)
    temp = out[:-7]

    basename0 = os.path.basename(temp)
    curdirpath = os.path.dirname(temp)
    temp0 = os.path.split(curdirpath)
    currdir = temp0[1]
    pardirpath = temp0[0]
    pardir = os.path.split(pardirpath)[1]
    if currdir == "aligned" and pardir == "aligned":
        temp = os.path.join(pardirpath, basename0)

    return temp


def test_1file():
    """Test 1 file."""
    file1 = "data/newsen.txt"
    # file2 = r'D:\dl\Dropbox\shuangyu_ku\txt-books\newszh.txt'

    out = twofiles_trunk(file1)
    expected = r"data/aligned/newsen"
    assert Path(out) == Path(expected).resolve()


def test_2files_():
    """Test 2 files."""
    file1 = "data/newsen.txt"
    file2 = "data/newszh.txt"

    out = twofiles_trunk(file1, file2)
    # expected = file1[:-6]
    # expected = r"D:\dl\Dropbox\shuangyu_ku\txt-books\aligned\news"
    expected = r"data/aligned/news"

    assert Path(out) == Path(expected).resolve()


def test_2filesa():
    """Test 2 files a."""
    file1 = "data/newszh.txt"
    file2 = "data/newsen.txt"

    out = twofiles_trunk(file1, file2)
    # expected = file1[:-6]
    expected = "data/aligned/news"

    assert Path(out) == Path(expected).resolve()


def test_aligned():
    """Test aligned."""
    fp = "D:\\dl\\Dropbox\\mat-dir\\snippets-mat\\pyqt\\Sandbox\\text_mat\\aligned\\text_enzh.txt"
    fp = "data/aligned/text_enzh.txt"
    exp = "data/aligned/text_enzh"
    assert Path(exp).resolve() == Path(twofiles_trunk(fp))
