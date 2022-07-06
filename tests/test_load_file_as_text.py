"""Test load_file_as_text."""
from ptextpad.loadtext import loadtext

from ptextpad.load_file_as_text import load_file_as_text


def test1():
    r"""Test default file.

    defaultdir = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt'
    defaultfile = r'notes pyqt tkinter tktable.txt'
    """
    filepath = r"C:\dl\Dropbox\mat-dir\pyqt\notes pyqt tkinter tktable.txt"
    text = loadtext(filepath)
    assert len(text) == 2283


def testgb():
    """
    Tests gb 爱丽丝漫游奇境记.txt.
    """
    file = r"C:\dl\Dropbox\shuangyu_ku\txt-books\19部世界名著中英文对照版TXT"
    file += r"\爱丽丝漫游奇境记.txt"
    text = loadtext(file)
    assert len(text) == 188763

    text0 = """ALICE'S ADVENTURES IN WONDERLAND\n CHAPTER  01  Down the Rabbit-Hole\n CHAPTER  02  The Pool of Tears\n CHAPTER  03  A Caucus-Race and a Long Tale\n CHAPTER  04  The Rabbit Sends in a Little Bill\n CHAPTER  05  Advice from a Caterpillar\n CHAPTER  06  Pig and Pepper\n CHAPTER  07  A Mad Tea-Party\n CHAPTER  08  The Queen's Croquet-Ground\n CHAPTER  09  The Mock Turtle's Story \n CHAPTER  10  The Lobster Quadrille\n CHAPTER  11  Who Stole the Tarts?\n CHAPTER  12  Alice's Evidence\n\n\n 爱 丽 丝 漫 游 奇 境 记 \n\n 第01章 掉进兔子洞 \n 第02章 眼泪的池塘 \n 第03章 一场会议"""
    assert text0 == text[:530]


def test_htm():
    """
    Test htm.
    """
    file = r"C:\dl\Dropbox\mat-dir\pyqt\Sandbox\test_files\files_for_testing_load\双语新闻(2017年2月3日).htm"  # NOQA
    text = load_file_as_text(file)
    # eq_(len(text), 7812)
    assert len(text) >= 7700  # 7762


def test_ass():
    """Test ass."""
    filepath = (r"C:\dl\Dropbox\mat-dir\pyqt\Sandbox\test_files"
    "\\files_for_testing_load"
    "\\The.Big.Bang.Theory.S10E15.720p.HDTV.X264-DIMENSION.ass")
    filepath = r"data\The.Big.Bang.Theory.S10E15.720p.HDTV.X264-DIMENSION.ass"  # 
    text = load_file_as_text(filepath)

    # eq_(19148, len(text))
    assert len(text) > 19000

    text0 = "我正在把微流控通道里的电渗流流速\nOkay, I'm zeroing out the electro-osmotic flow rate\n给归零了\nin the micro-fluidic chann"  # NOQA

    assert text.startswith(text0)


def test_pdf():
    """Test pdf.

    Refer to test_filepath1() in clapse_text
    """
    filepath = "C:\\dl\\Dropbox\\mat-dir\\pyqt\\Sandbox\\text_mat\\TE8-13期封面故事中英双语对照.pdf"  # NOQA
    text = load_file_as_text(filepath)
    exp = 94

    assert exp == len(text.splitlines())
