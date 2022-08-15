"""Convert epub to text."""
import logging
import os
import zipfile

# from element_to_string import element_to_string
from html2text import html2text

# from lxml import etree
# import zipfile
# from nose.tools import eq_, with_setup

from .post_process import post_process

# import re


# from bs4 import BeautifulSoup
# from htmlToText import htmlToText

# from html2txt import html2txt

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def epub_to_txt(fileepub):
    """
    Convert epub file to text str.

    use zipZip
    """

    if not os.path.exists(fileepub):
        LOGGER.warning(" File %s does not exist, return None.", fileepub)
        return None

    if not zipfile.is_zipfile(fileepub):
        LOGGER.warning(" File %s is not a zip file. Return None.", fileepub)
        return None

    try:
        zfile = zipfile.ZipFile(fileepub, "r")
    except Exception as exc:
        LOGGER.error(" Error: %s", exc)
        return None
    len0 = len(zfile.namelist())

    if not len0:
        LOGGER.warning(" zipfile.ZipFile(file).namelist() is empty, returning None.")
        return None

    text = ""
    for elm in zfile.namelist():
        if elm[-6:] == ".xhtml" or elm[-5:] == ".html":
            data = zfile.read(elm)
            # tree = etree.fromstring(data)
            # text += element_to_string(tree)

            text += html2text(data.decode())
            # text += html2txt(data)

            # soup = BeautifulSoup(data, 'lxml')
            # text += soup.get_text('\n')

    text = post_process(text)

    return text.strip()


def my_setup():
    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


# pep8/flake8/pyling filename
# nosetests -v --nologcapture
# @with_setup(my_setup)
def test_():
    fileepub = r"txt-books\Folding_Beijing-en1.epub"
    fileepub = "data/Folding_Beijing-en1.epub"

    assert epub_to_txt(fileepub) is None

    fileepub = r"txt-books\To Kill a Mockingbird\To Kill a Mockingbird.mobi"
    fileepub = "data/To Kill a Mockingbird\To Kill a Mockingbird.mobi"
    assert epub_to_txt(fileepub) is None

    fileepub = r"txt-books\Folding_Beijing-en.epub"
    fileepub = "data/Folding_Beijing-en.epub"
    _ = epub_to_txt(fileepub)
    assert len(_) >= 86400
