"""Realign list.

Refer to align_text, gen_aligned_sentlist in mypythonlib.
"""
import logging

from nose.tools import eq_, with_setup

# from para_gc import align_blocks_final
from .align_blocks_final import align_blocks_final
from .seg_sent import seg_sent

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def realign_list(lst, selected_rows, srclang="english", tgtlang="chinese"):
    """
    Realign list.

    :in: list, selected_rows
    :out: realigned 1st, 2nd column, '' if any for selected_rows only.

    Need to modify the list in mytable: pop and insert
    .tablemodel.layoutAboutToBeChanged.emit()
    ...
    .tablemodel.layoutChanged.emit()
    """
    # srctextlist
    # tgttextlist
    srctextlist = []
    tgttextlist = []

    for elm in selected_rows:
        srctextlist += lst[elm][0]
        tgttextlist += lst[elm][1]

    srctext = ""
    for elm in srctextlist:
        if elm.strip():
            srctext += elm.strip() + "\n"
    tgttext = ""
    for elm in tgttextlist:
        if elm.strip():
            tgttext += elm.strip() + "\n"

    srcsents = seg_sent(srctext, srclang)
    tgtsents = seg_sent(tgttext, tgtlang)

    # len1 = len(srcsents)
    # len2 = len(tgtsents)

    seq1 = [len(elm) for elm in srcsents if elm.strip()]
    seq2 = [len(elm) for elm in tgtsents if elm.strip()]

    alignvec = align_blocks_final(seq1, seq2)

    totse = srcsents[:]
    totsc = tgtsents[:]

    # for combining two sents
    auxch = ""
    if tgtlang != "chinese":
        auxch = " "

    srctgtvec = []
    ith0 = -1  # tmp var to help collect multiple totsc
    for vec in alignvec:
        if vec[0] == ith0:
            srctgtvec[ith0][1] += auxch + totsc[vec[1]]
        else:
            ith0 = vec[0]
            srctgtvec.append([totse[vec[0]], totsc[vec[1]]])

    # set col 3- to '' if any
    len0 = len(srctgtvec[0])
    for idx, elm in enumerate(srctgtvec):
        srctgtvec[idx] = srctgtvec[:2] + [""] * (len0 - 2)

    return srctgtvec


def my_setup():
    """my_setup."""
    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


@with_setup(my_setup)
def test_():
    """test_+++"""
    out = 1
    eq_(1, out)
    # LOGGER.debug(" %s ", var)
