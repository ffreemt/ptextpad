# encoding: utf-8
"""
Convert xml to text
"""
import os
import logging

from lxml import etree
# import zipfile
from nose.tools import (eq_, with_setup)

# from element_to_string import element_to_string

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def xml_to_txt(filepath):
    """
    Convert epub file to text str.

    use zipZip
    """

    if isinstance(filepath, str):
        if not os.path.exists(filepath):
            LOGGER.warning(" File %s does not exist, return None.", filepath[:50])
            return None

        try:
            doc = etree.parse(filepath)
        except Exception as exc:
            LOGGER.error(" etree.parse(filepath) error: %s, return None.", exc)
            return None
        docfindall = doc.findall('//')
    elif isinstance(filepath, bytes):  # supply bytes directly
        try:
            doc = etree.fromstring(filepath)
        except Exception as exc:
            LOGGER.error(" etree.fromstring error: %s, return None.", exc)
            return None
        docfindall = doc.getroottree().findall('//')
    else:
        LOGGER.warning(" Input not a file path nor bytes string, return None/")
        return None



    if not docfindall:
        LOGGER.warning(" doc.findall('//') is empty, returning None.")
        return None

    text = ''
    for elm in docfindall:
        text += elm.text if elm.text else ''
    text = text.strip()

    if not text:
        LOGGER.warning(" findall('//').text all empty, return empty (''). ")

    return text


def my_setup():
    """Setup."""
    fmt = '%(name)s-%(filename)s[ln:%(lineno)d]:'
    fmt += '%(levelname)s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.DEBUG)


# pep8/flake8/pyling filename
# nosetests -v --nologcapture
@with_setup(my_setup)
def test_():
    """special cases"""
    filepath = r'D:\dl\Dropbox\shuangyu_ku\txt-books\Folding_Beijing-en1.epub'

    eq_(None, xml_to_txt(filepath))

    filepath = r'D:\dl\Dropbox\shuangyu_ku\txt-books\To Kill a Mockingbird\To Kill a Mockingbird.mobi'
    eq_(None, xml_to_txt(filepath))

    filepath = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\neualignerv002\voanews.tmx'
    eq_(4522, len(xml_to_txt(filepath)))


@with_setup(my_setup)
def test_xml():
    """Test xml>>> """
    filepath = r'E:\beta_final_version\build\test_files\files_for_testing_load\越女剑-zh-en_2.xml'

    LOGGER.debug("Len: %s", len(xml_to_txt(filepath)))
    # filepath = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\neualignerv002\voanews.tmx'
    # eq_(4522, len(xml_to_txt(filepath)))
