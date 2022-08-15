"""
Docx to text based on docx (python-docx)
"""
import logging
import os

import docx
from nose.tools import eq_, with_setup

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def docx_to_text(filepath):
    """Convert docx to text based on python-docx."""
    if not os.path.exists(filepath):
        LOGGER.warning(" File %s does not exist...", filepath)
        return None
    try:
        docx_ = docx.Document(filepath)
    except Exception as exc:
        LOGGER.error(" Cannot open the file: %s", exc)
        return None
    text = ""
    for elm in docx_.paragraphs:
        print(elm.text)
        text += elm.text + "\n"
    return text


def my_setup():
    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


# pep8/flake8/pyling filename
# nosetests -v --nologcapture
@with_setup(my_setup)
def test_():
    """docx==>"""
    file = r"D:\dl\Dropbox\yeeyan\books\it-articles\2013-sep-it\2016-10-04_dual.docx"
    text = docx_to_text(file)
    eq_(3703, len(text))


@with_setup(my_setup)
def test_doc():
    """doc==>"""
    file = "D:\\dl\\Dropbox\\yeeyan\\books\\it-articles\\2013-sep-it\\2013-12-20-Oracle-dual-zh.doc"
    text = docx_to_text(file)
    eq_(None, text)
