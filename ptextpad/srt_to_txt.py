"""
Convert srt to text
"""
import logging
import os
import re

import chardet
import pysrt

# from lxml import etree
# import zipfile
from nose.tools import eq_, with_setup

# from element_to_string import element_to_string
from .detect_file import detect_file

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def srt_to_txt(filepath, list=False):
    """
    Convert srt file or bytes to text str.

    use pysrt
    """

    if isinstance(filepath, str):
        if not os.path.exists(filepath):
            LOGGER.warning(" File %s does not exist, return None.", filepath[:50])
            return None

        try:
            subs = pysrt.open(filepath, detect_file(filepath))
        except Exception as exc:
            LOGGER.error(
                " pysrt.open(filepath, detect_file(filepath)) error: %s, return None.",
                exc,
            )
            return None

    elif isinstance(filepath, bytes):  # supply bytes directly
        try:
            encoding = chardet.detect(filepath[:1000])["encoding"]
            subs = pysrt.from_string(filepath.decode(encoding))  # noqa
        except Exception as exc:
            LOGGER.error(
                " pysrt.from_string(filepath.decode(encoding) error: %s, return None.",
                exc,
            )
            return None
    else:
        LOGGER.warning(" Input not a file path nor bytes string, return None.")
        return None

    if not len(subs):
        LOGGER.warning(" len(subs) is 0, probably not srt, returning None.")
        return None

    # text = ''.join([elm.text.encode('gbk','replace').decode('gbk') for elm in subs])
    text = "_par_".join([elm.text for elm in subs])

    # lines = text.splitlines()
    # text = '\n\n'.join([elm.strip() for elm in lines if elm.strip()])  # noqa

    # lump together for cleaning up to save time?
    # < > </ > tags
    text = re.sub(r"</?.*?>", "", text)

    text = text.split("_par_")

    # text output
    if not list:
        text = "\n".join(text)

    return text


def my_setup():
    """Setup."""
    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


# pep8/flake8/pyling filename
# nosetests -v --nologcapture
@with_setup(my_setup)
def test_():
    """special cases"""
    filepath = r"D:\dl\Dropbox\shuangyu_ku\txt-books\Folding_Beijing-en1.epub"

    eq_(None, srt_to_txt(filepath))

    filepath = r"D:\dl\Dropbox\shuangyu_ku\txt-books\To Kill a Mockingbird\To Kill a Mockingbird.mobi"
    eq_(None, srt_to_txt(filepath))

    filepath = (
        r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\neualignerv002\voanews.tmx"
    )
    eq_(None, srt_to_txt(filepath))


@with_setup(my_setup)
def test_srt():
    """Test srt>>>"""
    filepath = (
        r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\test_files\ImKeller.chs.srt"
    )

    LOGGER.debug("Len: %s", len(srt_to_txt(filepath)))

    eq_(6683, len(srt_to_txt(filepath)))


@with_setup(my_setup)
def test_srtLuis():
    """Test Luis Trenker>>>"""
    filepath = r"F:\baiduyundownload\2015-11-18_ard_FilmMittwoch im Ersten - Luis Trenker - Der schmale Grat der Wahrheit@HD-default.srt"
    LOGGER.debug("Len: %s", len(srt_to_txt(filepath)))

    eq_(49684, len(srt_to_txt(filepath)))


@with_setup(my_setup)
def test_srtLuis_bytes():
    """Test Luis Trenker>>>"""
    filepath = r"F:\baiduyundownload\2015-11-18_ard_FilmMittwoch im Ersten - Luis Trenker - Der schmale Grat der Wahrheit@HD-default.srt"

    tmp = open(filepath, "rb").read()

    eq_(49684, len(srt_to_txt(tmp)))
