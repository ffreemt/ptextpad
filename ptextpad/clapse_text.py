# coding: utf-8
"""
Clapse text from pdftotext.
"""
import logging
import re

from fastlid import fastlid

from .pdf_to_text import pdf_to_text

# from detect_lang import detect_lang
# import langid
# from nose.tools import (eq_, with_setup)


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def clapse_text(text, preamble=" "):
    """
    Clapse texts (typically from pdftotext) to paras.

    premble (default = ' '): lines staring with preamble+ new para
    combine (default = True): combine lines inthe same language

    different languages: new para
    """

    # langid.set_languages(['en', 'zh'])
    fastlid.set_languages = ["en", "zh"]

    textvec = text.splitlines()

    # textid = [langid.classify(elm)[0] if elm.strip() else '' for elm in textvec]
    textid = [fastlid(elm)[0] if elm.strip() else "" for elm in textvec]

    texttemp = textvec[0]
    for idx, elm in enumerate(textvec[1:]):
        temp = ""
        if textid[idx + 1] == textid[idx]:
            if re.match(preamble, elm):
                temp += "\n"
            else:
                temp += (
                    "" if textid[idx + 1] == "zh" else " "
                )  # no space for chinese, space for english
        else:
            temp += "\n"
        temp += elm
        texttemp += temp

    return texttemp


def test_filepath1():
    """test_TE8-13期封面故事中英双语对照.pdf+++."""
    filepath1 = "D:\\dl\\Dropbox\\mat-dir\\snippets-mat\\pyqt"
    "\\Sandbox\\text_mat\\TE8-13期封面故事中英双语对照.pdf"
    filepath1 = "D:\\data\\TE8-13期封面故事中英双语对照.pdf"

    text1 = pdf_to_text(filepath1)

    text1a = clapse_text(text1)
    # In [556]: len(text1a.splitlines())
    # Out[556]: 94
    exp = 94
    # LOGGER.debug("test out: %s", out)

    assert exp == len(text1a.splitlines())
