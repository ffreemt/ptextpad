"""Segment non chinese."""
import logging
import os

# from pkg_resources import resource_stream
import pickle

# from nose.tools import (eq_, with_setup)


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


# def seg_xysent(text, language='english')->"tokenizer.tokenize(text)":
def seg_xysent(text, language="english"):
    """Segment New seg_xysent."""
    global TOK
    # from entokenizer import ENTOK as TOK
    langset = ["english", "french", "italian", "portugese", "spanish", "german"]
    """
    lang_abbr = ['EN', 'FR', 'IT', 'PT', 'ES', 'DE']
    lang_dict = dict(zip(langset, lang_abbr))

    test = 'this is a sent. This is another; A third'
    for elm in lang_dict:
        abbr = lang_dict.get(elm)
        TOK = importlib.import_module(abbr.lower() + 'tokenizer')
        tokenizer = getattr(TOK, abbr + 'TOK')
        print(abbr, tokenizer.tokenize(test))
    """

    if language not in langset:
        language = "english"

    # LOGGER.debug(" languge: %s", language)
    # LOGGER.debug(" type(TOK): %s", type(TOK))

    if language == "english":
        from entokenizer import ENTOK as TOK
    elif language == "german":
        from detokenizer import DETOK as TOK
    elif language == "french":
        from frtokenizer import FRTOK as TOK
    elif language == "portugese":
        from pttokenizer import PTTOK as TOK
    elif language == "italian":
        from ittokenizer import ITTOK as TOK
    else:  # language == 'spanish'
        from estokenizer import ESTOK as TOK

    # LOGGER.debug(" importing ... %s", importline)
    # exec(importline)

    # LOGGER.debug(" type(TOK): %s", type(TOK))

    if TOK is None:
        LOGGER.error(" TOK is none, return None")
        return None

    return TOK.tokenize(text)


def my_setup():
    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


# @with_setup(my_setup)
def test_():
    """test_."""
    sents = seg_xysent("this is a test. another sentence.")
    assert "this is a test." == sents[0]
    assert "another sentence." == sents[1]


# @with_setup(my_setup)
def test_foldingbj():
    """test_foldingbj."""
    import re
    import time

    from tqdm import tqdm

    file = r"D:\dl\Dropbox\shuangyu_ku\txt-books\Folding_Beijing-en.txt"  # noqa
    time1 = time.time()

    sents = []
    with open(file, "r", encoding="utf8") as filehandle:
        for idx, elm in enumerate(tqdm(filehandle.readlines())):
            sents += seg_xysent(elm.strip())
    assert 1112 == len(sents)

    LOGGER.debug("\n   1 Time used: %s", time.time() - time1)
    # 10 times faster!
    time1 = time.time()
    sents0 = seg_xysent(open(file, "r", encoding="utf8").read().strip())
    sents1 = []
    for elm in sents0:
        sents1 += re.split(r"\n+", elm)

    time1 = time.time()
    assert sents == sents1

    LOGGER.debug("\n   2 Time used: %s", time.time() - time1)


# @with_setup(my_setup)
def test_foldingbj1():
    """test_foldingbj1."""
    # from tqdm import tqdm
    import re
    import time

    file = r"D:\dl\Dropbox\shuangyu_ku\txt-books\Folding_Beijing-en.txt"  # noqa

    time1 = time.time()
    # much faster!
    texten = open(file, "r", encoding="utf8").read().strip()
    paras = re.split(r"\n+", texten)

    texten0 = re.sub(r"\n+", "_par_.", texten)

    sents0 = seg_xysent(texten0)

    text_res = "_sent_".join(sents0)
    para_sents = text_res.split("_par_.")

    sents2 = []
    for elm in para_sents:
        sents2 += elm.split("_sent_")

    para_sents_seg = []
    for elm in para_sents:
        para_sents_seg.append(elm.split("_sent_"))

    LOGGER.debug(" 3 Time used: %s", time.time() - time1)
    assert 294 == len(para_sents_seg)
    assert 1112 == len(sents2)

    # eq_(len(paras), len(para_sents))  # 294
    # eq_(len(paras), len(para_sents))  # 294

    # assert 1112 == sents1
