# encoding: utf-8
"""
Convert html str to txt.

Using html2text (md)
"""
import logging
import re

import chardet
from html2text import html2text
# from nose.tools import eq_, with_setup

from .post_process import post_process

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def html2txt(input):

    if isinstance(input, bytes):
        encoding = chardet.detect(input[:2000])["encoding"]
        input = input.decode(encoding, "ignore")

    if not isinstance(input, str):
        LOGGER.warning(" Input not str nor bytes, return None")
        return None

    text = html2text(input)

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
    filepath = "data/test.html"
    out = html2txt(open(filepath, "r", encoding="gbk").read())
    _ = len(out)
    assert _ > 4900  # 4982
