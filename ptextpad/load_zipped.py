# encoding: utf-8
"""
Load zipped text files.
"""
import logging
import os
import zipfile
from io import BytesIO

import chardet
from nose.tools import eq_, with_setup

from .docx_to_txt import docx_to_txt
from .html2txt import html2txt
from .srt_to_txt import srt_to_txt
from .srtass_to_txt import srtass_to_txt

# from element_to_string import element_to_string
# from load_text import load_text
from .xml_to_txt import xml_to_txt

# from io import StringIO
# from lxml import etree


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def load_zipped(filezip):
    """
    Load zipped text/html/htm/xhtml/docx, only load the first file.

    use zipZip
    """

    if not os.path.exists(filezip):
        LOGGER.warning(" File %s does not exist, return None.", filezip)
        return None

    if not zipfile.is_zipfile(filezip):
        LOGGER.warning(" File %s is not a zip file. Return None.", filezip)
        return None

    try:
        zfile = zipfile.ZipFile(filezip, "r")
    except Exception as exc:
        LOGGER.error(" Loadl as zipped file, error: %s", exc)
        return None

    len0 = len(zfile.namelist())

    if not len0:
        LOGGER.warning(" %s is empty, returning None.")
        return None

    text = ""
    for elm in zfile.namelist():
        # if elm[-4:] == '.txt' or elm[-4:] == '.htm' or elm[-5:] == '.html' or elm[-4:] == '.xml' or elm[-6:] == '.xhtml' or elm[-4:] == '.srt' or elm[-4:] == '.ass':  # noqa
        if elm.endswith(
            (".txt", ".htm", ".html", ".xml", ".xhtml", ".srt", ".ass")
        ):  # noqa
            break

    data = zfile.read(elm)  # epub META-INF/container.xml

    # text = html2txt(data)  # data is bytes string

    # wrapped as a file object:
    # datafile = StringIO(data)

    if elm[-4:] == ".txt":
        encoding = chardet.detect(data[:100])["encoding"]
        text = data.decode(encoding, "ignore")
        if not text:
            LOGGER.warning("The first text file is empty. Return empty ('')")
        return text
    elif elm[-4:] == ".xml":
        text = xml_to_txt(data).strip()
    elif elm[-5:] == ".docx":
        encoding = chardet.detect(data[:2000])["encoding"]
        fileobj = BytesIO(data)
        text = docx_to_txt(fileobj)
    elif elm[-4:] == ".srt":
        # encoding = chardet.detect(data[:2000])['encoding']
        text = srt_to_txt(data)
    elif elm[-4:] == ".ass":
        # encoding = chardet.detect(data[:2000])['encoding']
        text = srtass_to_txt(data)
    else:
        text = html2txt(data).strip()

    if not text:
        LOGGER.warning(
            "The first txt/html/htm/xml/xhtml/srt/ass/ file in the zip file does not contain any text. Return empty ('')"
        )
    return text


def my_setup():
    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


# pep8/flake8/pyling filename
# nosetests -v --nologcapture
@with_setup(my_setup)
def test_special_cases():
    """Test special cases >>>"""
    filezip = r"D:\dl\Dropbox\shuangyu_ku\txt-books\Folding_Beijing-en1.epub"

    eq_(None, load_zipped(filezip))

    filezip = r"D:\dl\Dropbox\shuangyu_ku\txt-books\To Kill a Mockingbird\To Kill a Mockingbird.mobi"
    eq_(None, load_zipped(filezip))

    filezip = r"D:\dl\Dropbox\shuangyu_ku\txt-books\Folding_Beijing-en.epub"
    eq_(0, len(load_zipped(filezip)))


@with_setup(my_setup)
def test_htmlzip():
    """Test html.zip>>>"""
    filezip = r"E:\beta_final_version\build\test_files\files_for_testing_load\双语新闻(2017年2月3日).zip"

    eq_(7807, len(load_zipped(filezip)))


@with_setup(my_setup)
def test_txtzip():
    """Test txt.zip>>>"""
    filezip = r"E:\beta_final_version\build\test_files\files_for_testing_load\voa_dual_txt.zip"
    out = load_zipped(filezip)
    eq_(1872, len(out))


@with_setup(my_setup)
def test_xmlzip():
    """Test xml.zip>>>"""
    filezip = r"E:\beta_final_version\build\test_files\files_for_testing_load\越女剑-zh-en_xml.zip"
    out = load_zipped(filezip)
    eq_(69680, len(out))


@with_setup(my_setup)
def test_docxzip():
    """Test docx.zip>>>"""
    filezip = r"E:\beta_final_version\build\test_files\files_for_testing_load\2012年3月经济学人文章_docx.zip"
    out = load_zipped(filezip)
    eq_(182949, len(out))


@with_setup(my_setup)
def test_srtzip():
    """Test srt.zip>>>"""
    filezip = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\test_files\ImKeller.chs.zip"  # noqa
    out = load_zipped(filezip)
    eq_(6683, len(out))


@with_setup(my_setup)
def test_asszip():
    """Test ass.zip>>>"""
    filezip = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\test_files\files_for_testing_load\The.Big.Bang.Theory.S10E15.720p.HDTV.X264-DIMENSIONass.zip"  # noqa
    out = load_zipped(filezip)
    eq_(19148, len(out))

    text0 = "我正在把微流控通道里的电渗流流速\nOkay, I'm zeroing out the electro-osmotic flow rate\n给归零了\nin the micro-fluidic chann"
    eq_(text0, out[:100])
