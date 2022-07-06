"""
Convert epub to text
"""
import os
import logging
# import re

import zipfile
# from lxml import etree
# import zipfile
from nose.tools import (eq_, with_setup)

# from element_to_string import element_to_string
from html2text import html2text

from .post_process import post_process

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
        zfile = zipfile.ZipFile(fileepub, 'r')
    except Exception as exc:
        LOGGER.error(" Error: %s", exc)
        return None
    len0 = len(zfile.namelist())

    if not len0:
        LOGGER.warning(" zipfile.ZipFile(file).namelist() is empty, returning None.")
        return None

    text = ''
    for elm in zfile.namelist():
        if elm[-6:] == '.xhtml' or elm[-5:] == '.html':
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
    fmt = '%(name)s-%(filename)s[ln:%(lineno)d]:'
    fmt += '%(levelname)s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.DEBUG)


# pep8/flake8/pyling filename
# nosetests -v --nologcapture
@with_setup(my_setup)
def test_():
    fileepub = r'D:\dl\Dropbox\shuangyu_ku\txt-books\Folding_Beijing-en1.epub'

    eq_(None, epub_to_txt(fileepub))

    fileepub = r'D:\dl\Dropbox\shuangyu_ku\txt-books\To Kill a Mockingbird\To Kill a Mockingbird.mobi'
    eq_(None, epub_to_txt(fileepub))

    fileepub = r'D:\dl\Dropbox\shuangyu_ku\txt-books\Folding_Beijing-en.epub'
    eq_(86745, len(epub_to_txt(fileepub)))
