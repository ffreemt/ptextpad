"""Test load_file_as_text."""
from ptextpad.loadtext import loadtext

from ptextpad.load_file_as_text import load_file_as_text


def test1():
    r"""Test default file.

    defaultdir = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt'
    defaultfile = r'notes pyqt tkinter tktable.txt'
    """
    filepath = r"C:\dl\Dropbox\mat-dir\pyqt\notes pyqt tkinter tktable.txt"
    filepath = r"data/newsen.txt"
    text = loadtext(filepath)
    assert len(text) >= 4545


def testgb():
    """
    Tests gb 爱丽丝漫游奇境记.txt.
    """
    file = r"data/爱丽丝漫游奇境记.txt"
    text = loadtext(file)
    assert len(text) >= 188763

    assert text.startswith("ALICE'S ADVENTURES IN WONDERLAND")


def test_htm():
    """
    Test htm.
    """
    file = r"C:\dl\Dropbox\mat-dir\pyqt\Sandbox\test_files\files_for_testing_load\双语新闻(2017年2月3日).htm"  # NOQA
    file = r"data/双语新闻.htm"

    text = load_file_as_text(file)
    assert len(text) >= 7700  # 7762


def test_ass():
    """Test ass."""
    filepath = (
        r"C:\dl\Dropbox\mat-dir\pyqt\Sandbox\test_files"
        "\\files_for_testing_load"
        "\\The.Big.Bang.Theory.S10E15.720p.HDTV.X264-DIMENSION.ass"
    )
    filepath = r"data\The.Big.Bang.Theory.S10E15.720p.HDTV.X264-DIMENSION.ass"  #
    text = load_file_as_text(filepath)

    # eq_(19148, len(text))
    # assert len(text) > 19000  # FIXME

    text0 = "我正在把微流控通道里的电渗流流速\nOkay, I'm zeroing out the electro-osmotic flow rate\n给归零了\nin the micro-fluidic chann"  # NOQA

    # assert text.startswithq(text0)  # FIXME


def test_pdf():
    """Test pdf.

    Refer to test_filepath1() in clapse_text
    """
    filepath = "C:\\dl\\Dropbox\\mat-dir\\pyqt\\Sandbox\\text_mat\\TE8-13期封面故事中英双语对照.pdf"  # NOQA
    filepath = "data/TE8-13期封面故事中英双语对照.pdf"  # NOQA
    text = load_file_as_text(filepath)
    exp = 94

    # assert exp == len(text.splitlines())  # FIXME
