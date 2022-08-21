"""Align texts (srctext, tgttext, srclang=srclang, tgtlang=tgtlang)."""
import logging

# from nose.tools import (eq_, with_setup)

# from .seg_sent import seg_sent
from seg_text import seg_text as seg_sent

from .detect_lang import detect_lang

# from .para_gc import align_blocks_final
from .align_blocks_final import align_blocks_final

from .load_text import load_text

# from para_gc import check_avec

from .zip_longest_middle import zip_longest_middle

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def align_text(srctext, tgttext, srclang="english", tgtlang="chinese", ratio_diff=1.0):
    """Output.

    nx2 list of srcsents and tgtsents
    """

    srcsents = seg_sent(srctext, srclang)
    tgtsents = seg_sent(tgttext, tgtlang)

    len1 = len(srcsents)
    len2 = len(tgtsents)

    if len1 + len2 == 0:  # both 0
        return None

    if len1 * len2 == 0:  # either 0
        srctgtvec = zip_longest_middle(srcsents, tgtsents, fillvalue="")

    if abs(len1 - len2) / max(len1, len2) >= ratio_diff:
        out = zip_longest_middle(srcsents, tgtsents, fillvalue="")
        srctgtvec = []
        for elm in out:
            srctgtvec.append([elm[0], elm[1]])
        return srctgtvec

    # for combining two sents
    auxch = " "
    if tgtlang == "chinese":
        auxch = ""

    s1 = [len(elm) for elm in srcsents if elm.strip()]
    s2 = [len(elm) for elm in tgtsents if elm.strip()]

    alignvec = align_blocks_final(s1, s2)

    totsc = tgtsents[:]
    totse = srcsents[:]

    # ecsents = []
    # i0 = -1  # tmp var to help collect multiple totsc
    # for vec in alignvec:

    # if vec[0] == i0:
    # ecsents[i0] += totsc[vec[1]]
    # else:
    # i0 = vec[0]
    # ecsents.append(totse[vec[0]]+'\t'+totsc[vec[1]])
    # [refer to align_sent_modi.py]

    srctgtvec = []
    ith0 = -1  # tmp var to help collect multiple totsc
    for vec in alignvec:
        if vec[0] == ith0:
            srctgtvec[ith0][1] += auxch + totsc[vec[1]]
        else:
            ith0 = vec[0]
            srctgtvec.append([totse[vec[0]], totsc[vec[1]]])

    return srctgtvec


def align_text0(srctext, tgttext, srclang="engilsh", tgtlang="chinese"):
    """Compare test using text."""

    srcsents = seg_sent(srctext, srclang)
    tgtsents = seg_sent(tgttext, tgtlang)

    # for combining two sents
    auxch = " "
    if tgtlang == "chinese":
        auxch = ""

    s1 = [len(elm) for elm in srcsents if elm.strip()]
    s2 = [len(elm) for elm in tgtsents if elm.strip()]

    alignvec = align_blocks_final(s1, s2)

    totsc = tgtsents[:]
    totse = srcsents[:]

    ecsents = []
    i0 = -1  # tmp var to help collect multiple totsc
    for vec in alignvec:

        if vec[0] == i0:
            ecsents[i0] += auxch + totsc[vec[1]]
        else:
            i0 = vec[0]
            ecsents.append(totse[vec[0]] + "\t" + totsc[vec[1]])
    # [refer to align_sent_modi.py]

    # srctgtvec = []
    # ith0 = -1 # tmp var to help collect multiple totsc
    # for vec in alignvec:
    # if vec[0] == ith0:
    # srctgtvec[ith0] += auxch + totsc[vec[1]]
    # else:
    # ith0 = vec[0]
    # srctgtvec.append([totse[vec[0]], totsc[vec[1]]])

    # return srctgtvec
    return ecsents


# @with_setup(my_setup)
def test_00():
    r"""Test 00.

    D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\splitbutton\news
    """
    # fileen = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\splitbutton\newsen.txt"
    # filezh = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\splitbutton\newszh.txt"
    fileen = "data/newsen.txt"
    filezh = "data/newszh.txt"

    text1 = load_text(fileen)
    text2 = load_text(filezh)

    srclang = detect_lang(text1)
    tgtlang = detect_lang(text2)

    out = align_text(text1, text2, srclang=srclang, tgtlang=tgtlang)
    # LOGGER.debug(" out \n%s ", out)

    out0 = align_text0(text1, text2, srclang=srclang, tgtlang=tgtlang)

    assert len(out) == len(out0)

    for ith, elm in enumerate(out):
        out1ith = out0[ith].split("\t")
        LOGGER.debug(" %s 0: out[ith][0] %s, out0[0] %s", ith, out[ith][0], out1ith[0])
        assert out[ith][0] == out1ith[0]

        LOGGER.debug(" %s 0: out[ith][1] %s, out0[1] %s", ith, out[ith][1], out1ith[1])
        assert out[ith][1] == out1ith[1]


# @with_setup(my_setup)
def test_01():
    """Test 01 Folding_Beijing_ch1."""
    # fileen = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\splitbutton\newsen.txt'
    # filezh = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\splitbutton\newszh.txt'
    fileen = r"E:\neualigner\Folding_Beijing_ch1-en.txt"
    filezh = r"E:\neualigner\Folding_Beijing_ch1-zh.txt"
    fileen = "data/Folding_Beijing_ch1-en.txt"
    filezh = "data/Folding_Beijing_ch1-zh.txt"

    text1 = load_text(fileen)
    text2 = load_text(filezh)

    srclang = detect_lang(text1)
    tgtlang = detect_lang(text2)

    out = align_text(text1, text2, srclang=srclang, tgtlang=tgtlang)
    # LOGGER.debug(" out \n%s ", out)

    out0 = align_text0(text1, text2, srclang=srclang, tgtlang=tgtlang)

    assert len(out) == len(out0)

    for ith, elm in enumerate(out):
        out1ith = out0[ith].split("\t")
        LOGGER.debug(" %s 0: out[ith][0] %s, out0[0] %s", ith, out[ith][0], out1ith[0])
        assert out[ith][0] == out1ith[0]

        LOGGER.debug(" %s 0: out[ith][1] %s, out0[1] %s", ith, out[ith][1], out1ith[1])
        assert out[ith][1] == out1ith[1]
