"""Convert srt to text."""
import logging
import os
import re
import tempfile

import chardet

# import pysrt
import pysubs2

# from lxml import etree
# import zipfile
# from nose.tools import eq_, with_setup

# from element_to_string import element_to_string
from .detect_file import detect_file
from .srt_to_txt import srt_to_txt

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


# http://stackoverflow.com/questions/15169101/how-to-create-a-temporary-file-that-can-be-read-by-a-subprocess/15235559#15235559
def temp_opener(name, flag, mode=0o777):
    return os.open(name, flag | os.O_TEMPORARY, mode)


def srtass_to_txt(filepath, list=False):
    """Convert srt file or bytes to text str.

    use pysrt
    """

    if isinstance(filepath, str):
        if not os.path.exists(filepath):
            LOGGER.warning(" File %s does not exist, return None.", filepath[:50])
            return None

        try:
            # subs = pysrt.open(filepath, detect_file(filepath))
            # encoding = detect_file(filepath).get("encoding")
            encoding = detect_file(filepath)
            if not encoding:
                raise Exception("Cant detect file type, binary file?")

            subs = pysubs2.load(filepath, encoding)
        except Exception as exc:
            # LOGGER.error(" pysrt.open(filepath, detect_file(filepath)) error: %s, return None.", exc)
            LOGGER.error(
                " pysubs2.load(filepath, detect_file(filepath)) error: %s, return None.",
                exc,
            )
            return None

    elif isinstance(filepath, bytes):  # supply bytes directly
        try:
            encoding = chardet.detect(filepath[:1000])["encoding"]
            # subs = pysrt.from_string(filepath.decode(encoding))  # noqa
            str_ = filepath.decode(encoding)  # string
        except Exception as exc:
            LOGGER.debug(" encoding = chardet.detect/decode(encoding) error: %s", exc)

        try:
            # dirpath = tempfile.mkdtemp()
            # with tempfile.mkdtemp() as dirpath:
            with tempfile.TemporaryDirectory() as dirpath:
                filepath1 = os.path.join(dirpath, "tmp.ass")
                with open(filepath1, "w", encoding=encoding) as fhandle:
                    fhandle.write(str_)

                # subs = pysrt.from_string(filepath1.decode(encoding))  # noqa
                subs = pysubs2.load(filepath1, encoding=encoding)  # noqa

        except Exception as exc:
            # LOGGER.error(" pysrt.from_string(filepath.decode(encoding) error: %s, return None.", exc)
            LOGGER.error(
                " with temp.mktemp()/pysubs2.load() error: %s, return None.", exc
            )
            return None
    else:
        LOGGER.warning(" Input not a file path nor bytes string, return None.")
        return None

    if not len(subs):
        LOGGER.warning(" len(subs) is 0, probably not srt nor ass, returning None.")
        return None

    # text = ''.join([elm.text.encode('gbk','replace').decode('gbk') for elm in subs])
    # text = '_par_'.join([elm.text for elm in subs])
    text = "_par_".join([elm.plaintext for elm in subs])

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


def test_():
    """special cases"""
    filepath = r"D:\dl\Dropbox\shuangyu_ku\txt-books\Folding_Beijing-en1.epub"

    assert srt_to_txt(filepath) is None

    filepath = r"D:\dl\Dropbox\shuangyu_ku\txt-books\To Kill a Mockingbird\To Kill a Mockingbird.mobi"
    assert srt_to_txt(filepath) is None

    filepath = (
        r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\neualignerv002\voanews.tmx"
    )
    assert srt_to_txt(filepath) is None


# @with_setup(my_setup)
def test_srt():
    """Test srt>>>"""
    filepath = (
        r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\test_files\ImKeller.chs.srt"
    )

    LOGGER.debug("Len: %s", len(srt_to_txt(filepath)))

    assert 6683 == len(srt_to_txt(filepath))


# @with_setup(my_setup)
def test_srtLuis():
    """Test Luis Trenker>>>"""
    filepath = r"F:\baiduyundownload\2015-11-18_ard_FilmMittwoch im Ersten - Luis Trenker - Der schmale Grat der Wahrheit@HD-default.srt"
    LOGGER.debug("Len: %s", len(srt_to_txt(filepath)))

    assert 49684 == len(srt_to_txt(filepath))


# @with_setup(my_setup)
def test_srtLuis_bytes():
    """Test Luis Trenker>>>"""
    filepath = r"F:\baiduyundownload\2015-11-18_ard_FilmMittwoch im Ersten - Luis Trenker - Der schmale Grat der Wahrheit@HD-default.srt"

    tmp = open(filepath, "rb").read()

    assert 49684 == len(srt_to_txt(tmp))


# @with_setup(my_setup)
def test_ass():
    """Test ass>>>"""
    filepath = r"F:\baiduyundownload\2015-11-18_ard_FilmMittwoch im Ersten - Luis Trenker - Der schmale Grat der Wahrheit@HD-default.srt"
    filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\test_files\files_for_testing_load\The.Big.Bang.Theory.S10E15.720p.HDTV.X264-DIMENSION.ass"

    # tmp = open(filepath, 'rb').read()

    assert 19148 == len(srtass_to_txt(filepath))


# @with_setup(my_setup)
def test_srtass():
    """Test srtass srt>>>"""
    filepath = (
        r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\test_files\ImKeller.chs.srt"
    )

    # LOGGER.debug("Len: %s", len(srt_to_txt(filepath)))
    tmp = srtass_to_txt(filepath)
    LOGGER.debug("Len: %s", len(tmp))

    # assert 6683 == len(srt_to_txt(filepath))
    assert 6817 == len(tmp)


# @with_setup(my_setup)
def test_srtasszip():
    """Test srtass srt zipped>>>"""
    import zipfile

    filezip = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\test_files\files_for_testing_load\The.Big.Bang.Theory.S10E15.720p.HDTV.X264-DIMENSIONass.zip"
    zfile = zipfile.ZipFile(filezip, "r")
    for elm in zfile.namelist():
        if (
            elm[-4:] == ".txt"
            or elm[-4:] == ".htm"
            or elm[-5:] == ".html"
            or elm[-4:] == ".xml"
            or elm[-6:] == ".xhtml"
            or elm[-4:] == ".srt"
            or elm[-4:] == ".ass"
        ):  # noqa
            break
    data = zfile.read(elm)
    text = srtass_to_txt(data)

    assert 6817 == len(text)
