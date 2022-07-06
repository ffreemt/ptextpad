"""Test load_text."""
from ptextpad.load_text import load_text


def test1():
    r"""
    Tests default file.

    defaultdir = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt'
    defaultfile = r'notes pyqt tkinter tktable.txt'
    """
    file = "data/newsen.txt"
    text = load_text(file)
    assert len(text) >= 4545


def testgb():
    r"""
    Tests  D:\dl\Dropbox\shuangyu_ku\txt-books\19部世界名著中英文对照版TXT
    """
    file = (
        r"C:\dl\Dropbox\shuangyu_ku\txt-books\19部世界名著中英文对照版TXT"
        r"\爱丽丝漫游奇境记.txt"
    )
    file = "data/爱丽丝漫游奇境记.txt"
    text = load_text(file)
    assert len(text) >= 188763

    assert text.startswith("ALICE'S ADVENTURES IN WONDERLAND")


def testUTF_16LE():
    r"""Test Folding_Beijing_12.txt'."""
    file = "E:\\beta_final_version\\build\\test_files"
    "\\files_for_testing_import\\Folding_Beijing_12.txt"
    file = "data/Folding_Beijing_12.txt"
    text = load_text(file)
    assert len(text) == 117871

    assert text.startswith("Folding Beijing\t北京折叠")
