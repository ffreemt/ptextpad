"""Test load_text."""
from ptextpad.load_text import load_text


def eq_(x, y):
    exec(f"assert {x} == {y}")


def test1():
    r"""
    Tests default file.

    defaultdir = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt'
    defaultfile = r'notes pyqt tkinter tktable.txt'
    """
    file = r"D:\dl\Dropbox\mat-dir\pyqt\notes pyqt tkinter tktable.txt"
    text = load_text(file)
    eq_(2283, len(text))


def testgb():
    r"""
    Tests  D:\dl\Dropbox\shuangyu_ku\txt-books\19部世界名著中英文对照版TXT
    """
    file = r"C:\dl\Dropbox\shuangyu_ku\txt-books\19部世界名著中英文对照版TXT"
    file += r"\爱丽丝漫游奇境记.txt"
    text = load_text(file)
    eq_(190913, len(text))

    text0 = r"ALICE'S ADVENTURES IN WONDERLAND\r\n CHAPTER  01  Down the Rabbit-Hole\r\n CHAPTER  02  The Pool of Tears\r\n CHAPTER  03  A Caucus-Race and a Long Tale\r\n CHAPTER  04  The Rabbit Sends in a Little Bill\r\n CHAPTER  05  Advice from a Caterpillar\r\n CHAPTER  06  Pig and Pepper\r\n CHAPTER  07  A Mad Tea-Party\r\n CHAPTER  08  The Queen's Croquet-Ground\r\n CHAPTER  09  The Mock Turtle's Story \r\n CHAPTER  10  The Lobster Quadrille\r\n CHAPTER  11  Who Stole the Tarts?\r\n CHAPTER  12  Alice's Evidence\r\n\r\n\r\n 爱 丽 丝 漫 游"  # NOQA
    eq_(text0, text[:500])


def testUTF_16LE():
    r"""
    Test  'E:\\beta_final_version\\build\\test_files\\files_for_testing_import\\Folding_Beijing_12.txt'.
    """
    file = "E:\\beta_final_version\\build\\test_files\\files_for_testing_import\\Folding_Beijing_12.txt"  # NOQA
    text = load_text(file)
    eq_(len(text), 117871)

    # text0 = '\ufeffFolding Beijing\t北京折叠\n"by Hao Jingfang, translated by Ken Liu"\t郝景芳\n# 1.\t# 1\n"At ten of five in the m'  # NOQA
    text0 = r'Folding Beijing\t北京折叠\n"by Hao Jingfang, translated by Ken Liu"\t郝景芳\n# 1.\t# 1\n"At ten of five in the mo'  # NOQA

    eq_(text0, text[:100])
