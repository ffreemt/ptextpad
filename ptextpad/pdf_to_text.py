# coding： utf8
"""
## git  D:\Program Files\Git\mingw32\bin\pdftotext.exe
pdftotext -h

pdftotext -nopgbrk test.pdf

pdftotext -nopgbrk -layout -enc UTF-8 test.pdf
        ! chinese OK

pdftotext -nopgbrk -layout test.pdf
            \r\n\r\n ==> _para_
            \r\n => ''
            _para_ => \r\n\r\n

  !!!fast

Usage: pdftotext [options] <PDF-file> [<text-file>]
  -f <int>             : first page to convert
  -l <int>             : last page to convert
  -layout              : maintain original physical layout
  -table               : similar to -layout, but optimized for tables
  -lineprinter         : use strict fixed-pitch/height layout
  -raw                 : keep strings in content stream order
  -fixed <fp>          : assume fixed-pitch (or tabular) text
  -linespacing <fp>    : fixed line spacing for LinePrinter mode
  -clip                : separate clipped text
  -enc <string>        : output text encoding name
  -eol <string>        : output end-of-line convention (unix, dos, or mac)
  -nopgbrk             : don't insert page breaks between pages
  -opw <string>        : owner password (for encrypted files)
  -upw <string>        : user password (for encrypted files)
  -q                   : don't print any messages or errors
  -cfg <string>        : configuration file to use in place of .xpdfrc
  -v                   : print copyright and version info
  -h                   : print usage information
  -help                : print usage information
  --help               : print usage information
  -?                   : print usage information
"""

import os
import logging
import subprocess
import tempfile

from nose.tools import (eq_, with_setup)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def pdf_to_text(filepath, pages=None)->"a string":
    """
    Convert a pdf file to text using pdftotext.exe.

    pdf_to_text(filepatah, [pages])->"a string"

    """
    if not isinstance(filepath, str):
        LOGGER.warning(" Input %s not a string. Return None", filepath)
        return None
    if not os.path.exists(filepath):
        LOGGER.warning("File :%s: does not exist, Retunr None", filepath)
        return None
    # currdir = os.path.dirname(os.path.abspath(__file__))
    # pdftotextcmd = currdir + 'pdftotext.exe'

    pdftotext1 = 'pdftotext.exe'

    def get_page(page):
        '''
        Get one page
        '''

        # outputTf = tempfile.NamedTemporaryFile()
        # outputTf = tempfile.NamedTemporaryFile(mode="r+")

        # cmdline0 = ['D:\\Program Files\\Git\\mingw32\\bin\\pdftotext.exe', '-f 1', '-l 1', 'D:\\dl\\Dropbox\\mat-dir\\snippets-mat\\pyqt\\Sandbox\\text_mat\\Amy Wall, Regina Wall-The Complete Idiots Guide to Critical Reading-Alpha (2005).pdf']
        # cmdline = ['D:\\Program Files\\Git\\mingw32\\bin\\pdftotext.exe', '-f 1', '-l 1', 'D:\\dl\\Dropbox\\mat-dir\\snippets-mat\\pyqt\\Sandbox\\text_mat\\Amy Wall, Regina Wall-The Complete Idiots Guide to Critical Reading-Alpha (2005).pdf', 'test00.txt']

        # pdftotext2.exe -f 2 -l 13 -nopgbrk -layout "经济学人特别报告：2030年的中国消费者（中文版）.pdf" # run ok

        # os.system(cmdline)
        cmdline1 = pdftotext1 + ' -f ' + str(page) + ' -l ' + str(page) + \
                    ' -nopgbrk -layout -enc UTF-8 ' + filepath
        text = ''
        with tempfile.TemporaryDirectory() as dirpath:
            outfile = os.path.join(dirpath,'testtmp.txt')

            try:
                LOGGER.debug(" os.system(%s + ' ' + %s) ", cmdline1, outfile)

                os.system(cmdline1 + ' ' + outfile)
            except Exception as exc:
                LOGGER.warning(" os.system(%s + ' ' + outfile) error: %s", cmdline1, exc)
                LOGGER.warning(" Return ''")

            if os.path.exists(outfile):
                with open(outfile, 'r', encoding='utf-8') as fhandle:
                    text = fhandle.read()
            else:
                LOGGER.warning(" pdftotext cannot convert Page %s to text. Return ''", page)
                return ''

            # text = outputTf.read()

            LOGGER.debug(" text: %s", text[:10])
        return text

    # >>> output = subprocess.check_output(['ls','-l'])

    text = ''
    if pages:
        for page in pages:
            text += get_page(str(page))
    else:
        cmdline1 = pdftotext1 + ' -nopgbrk -layout -enc UTF-8 ' + filepath
        with tempfile.TemporaryDirectory() as dirpath:
            # outfile = os.path.join(dirpath.name,'testtmp.txt')

            # pdf_to_text.exe cant seem to handle files with unicode
            # make a copy
            infile = os.path.join(dirpath, 'test.pdf')
            with open(infile, 'wb') as infilehandle:
                infilehandle.write(open(filepath, 'rb').read())

            outfile = os.path.join(dirpath, 'testtmp.txt')
            try:
                # text = subprocess.check_output([pdftotextexe, filepath, ' -nopgbrk '])
                cmdline1 = pdftotext1 + ' -nopgbrk -layout -enc UTF-8 ' + infile

                os.system(cmdline1 + ' ' + outfile)
            except Exception as exc:
                LOGGER.debug(" os.system(%s + ' ' + outfile), error: %s", cmdline1, exc)
                return None
            if os.path.exists(outfile):
                with open(outfile, 'r', encoding='utf-8') as fhandle:
                    text = fhandle.read()
            else:
                LOGGER.debug(" pdftotext probably did not output anything.")
                LOGGER.debug(" The file may not be a pdf or is password protect, or is a scanned file which will need OCR to obtain its text.")
                LOGGER.debug("Return None.")
                return None
    return text


def my_setup():
    """my_setup."""

    fmt = '%(name)s-%(filename)s[ln:%(lineno)d]:'
    fmt += '%(levelname)s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.DEBUG)


@with_setup(my_setup)
def test_daode():
    """test_《道德经》中英文对照版+++."""

    # pdftotext -f 1 -l 1 -layout -nopgbrk  # cmdline ok
    # pdftotext -f 1 -l 1 -layout -nopgbrk  test.pdf test1.txt # cmdline ok

    # filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\Amy Wall, Regina Wall-The Complete Idiots Guide to Critical Reading-Alpha (2005).pdf"
    filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\test.pdf"
    out = pdf_to_text(filepath, [1])

    # LOGGER.debug("len: %s, %s", len(out), out)
    exp = 1658
    eq_(exp, len(out))


@with_setup(my_setup)
def test_te_zh():
    """test_te chinese+++."""

    # pdftotext -f 1 -l 1 -layout -nopgbrk  # cmdline ok
    # pdftotext -f 1 -l 1 -layout -nopgbrk  test.pdf test1.txt # cmdline ok

    # filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\Amy Wall, Regina Wall-The Complete Idiots Guide to Critical Reading-Alpha (2005).pdf"
    filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\经济学人特别报告：2030年的中国消费者（中文版）.pdf"
    out = pdf_to_text(filepath, [1])

    # LOGGER.debug("len: %s, %s", len(out), out)
    exp = 26
    eq_(exp, len(out))


@with_setup(my_setup)
def test_te_zhfull():
    """test_te chinese full+++."""

    # pdftotext -f 1 -l 1 -layout -nopgbrk  # cmdline ok
    # pdftotext -f 1 -l 1 -layout -nopgbrk  test.pdf test1.txt # cmdline ok

    # filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\Amy Wall, Regina Wall-The Complete Idiots Guide to Critical Reading-Alpha (2005).pdf"
    filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\经济学人特别报告：2030年的中国消费者（中文版）.pdf"
    out = pdf_to_text(filepath)

    # LOGGER.debug("len: %s, %s", len(out), out)
    exp = 34900
    eq_(exp, len(out))


@with_setup(my_setup)
def test_te_en():
    """test_te en+++."""

    # pdftotext -f 1 -l 1 -layout -nopgbrk  # cmdline ok
    # pdftotext -f 1 -l 1 -layout -nopgbrk  test.pdf test1.txt # cmdline ok

    # filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\Amy Wall, Regina Wall-The Complete Idiots Guide to Critical Reading-Alpha (2005).pdf"
    filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\经济学人特别报告：2030年的中国消费者（英文版）.pdf"
    out = pdf_to_text(filepath, [4])

    # LOGGER.debug("len: %s, %s", len(out), out)
    exp = 3989
    eq_(exp, len(out))


@with_setup(my_setup)
def test_non_convertable_file_p1():
    """test_non_convertable_file p1+++."""
    filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\西遊記英文.epub"
    out = pdf_to_text(filepath, [1])
    exp = ''
    eq_(exp, out)


@with_setup(my_setup)
def test_non_convertable_file():
    """test_non_convertable_file+++."""
    filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\西遊記英文.epub"
    out = pdf_to_text(filepath)
    exp = None
    eq_(exp, out)

"""
In [76]: filepath
Out[76]: 'D:\\dl\\Dropbox\\mat-dir\\snippets-mat\\pyqt\\Sandbox\\test_files\\原版外刊双语精读材料 本期《The New York Times》精选 2016.10.17.pdf'

In [77]: filepath1
Out[77]: 'D:\\dl\\Dropbox\\mat-dir\\snippets-mat\\pyqt\\Sandbox\\text_mat\\TE8-13期封面故事中英双语对照.pdf'

In [78]: filepath2
Out[78]: 'D:\\dl\\Dropbox\\mat-dir\\snippets-mat\\pyqt\\Sandbox\\text_mat\\test.pdf'

In [64]: text2 = pdf_to_text(filepath2)

In [65]: len(text2)
Out[65]: 7160

In [66]: text = pdf_to_text(filepath)

In [67]: len(text)
Out[67]: 12797

In [68]: filepath1 = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\text_mat\TE8-13期封面故事中英双语对照.pdf'

In [69]: text1 = pdf_to_text(filepath1)

In [70]: len(text1)
Out[70]: 10100

"""