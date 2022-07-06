'''Converts two texts to  nx3 array.

aligned paras with  anchors as the 3rd column.

texts (source text and target text) obtained by
get_para.

Refer to set_anchors.py
'''
import logging

# from itertools import zip_longest
from zip_longest_middle import zip_longest_middle

# from guess_zhencoding import guess_zhencoding
# from get_para import get_para

from text_to_paras import text_to_paras
from load_text import load_text

from para_cosine_rev import para_cosine
from youdao_tr_list import youdao_tr_list
from detect_lang import detect_lang
from set_loglevel import set_loglevel

from align_sent import ccmatrix_th

# from logging_progress import logging_progress
# from tqdmlogginghandler import TqdmLoggingHandler


# from nose.tools import (eq_, with_setup)
def eq_(x, y): assert x == y


LOGGER = logging.getLogger(__name__)

# LOGGER.addHandler(TqdmLoggingHandler())
LOGGER.addHandler(logging.NullHandler())

FORMAT = '%(name)s - %(filename)s [line:%(lineno)d]'
FORMAT += '%(asctime)s:%(levelname)s:%(message)s'
logging.basicConfig(format=FORMAT, level=set_loglevel())


def texts_to_anchored_paras(text1, text2, tgtlang=None):
    # seqgl = list(map(lambda enseq: nettr(enseq), seq1))
    seq1 = text_to_paras(text1)
    seq2 = text_to_paras(text2)
    seqgl = []

    # LOGGER.debug("seq1: %s", seq1)
    # LOGGER.debug("seq2: %s", seq2)

    LOGGER.debug("seq1: %s...%s", seq1[:2], seq1[-2:])
    LOGGER.debug("seq2: %s...%s", seq2[:2], seq2[-2:])

    lenseq1 = len(seq1)

    """
    # for ielm, elm in enumerate(tqdm(seq1)):
    for ielm, elm in enumerate(seq1):
        seqgl += [nettr(elm)]
        # LOGGER.debug(" i: {}  seq1: {} ".format(ielm, elm))
        # LOGGER.info(" Fetching %s of %s", ielm + 1, lenseq1)
        logging_progress(ielm, lenseq1, bar_length=15)
    LOGGER.debug("^ net service ^")
    """

    # detect tgtlang if not specified
    if tgtlang is None:
        tgtlang = detect_lang(text2[:2000])
    # modi 2017 02 09

    seqgl = youdao_tr_list(seq1)

    if seqgl:
        LOGGER.debug(" seqgl[0] %s, ..., seqgl[-1]: %s \n", seqgl[0], seqgl[-1])  # noqa

    # LOGGER.debug("seqgl: %s", seqgl)
    # LOGGER.debug("seq2: %s", seq2)

    extra0 = min(10, abs(len(seq1) - len(seq2)))

    # ccmatrix = para_cosine(seqgl, seq2, extra0, tgt)
    ccmatrix = para_cosine(seqgl, seq2, extra0, tgtlang)  # modi noqa
    LOGGER.debug(" **possbile crash point? ** ")

    ccmatrixij0 = ccmatrix_th(ccmatrix)
    # LOGGER.debug(' ccmatrixij: %s ' % ccmatrixij0)
    # LOGGER.debug('\n Coming up...\n')

    # return ccmatrixij0

    lencc = len(ccmatrixij0)

    # empty ccmatrixij0
    if lencc == 0:
        zip12 = zip_longest_middle(seq1, seq2, fillvalue='')
        out = [list(elm)+[''] for elm in zip12]
        out[0][2] = 0.01
        out[-1][2] = 0.01
        return out
    '''list(zip_longest_middle([1,2], [3],fillvalue=''))
    modified to put '' in the middle
    '''
    ppos1 = 0
    ppos2 = 0
    len1 = len(seq1)
    len2 = len(seq2)
    aligned_seqs = []

    for pos in range(lencc):
        # aligned_seqs += zip_longest_middle(seq1[ppos1:ccmatrixij0[pos][0]], seq2[ppos2:ccmatrixij0[pos][1]], fillvalue='')  # noqa
        aligned_seqs += zip_longest_middle(seq1[ppos1:ccmatrixij0[pos][0]], seq2[ppos2:ccmatrixij0[pos][1]], fillvalue='')  # noqa
        ppos1 = ccmatrixij0[pos][0]
        ppos2 = ccmatrixij0[pos][1]
    aligned_seqs += zip_longest_middle(seq1[ppos1:len1], seq2[ppos2:len2], fillvalue='')  # noqa

    seq1a = [elm[0] for elm in aligned_seqs]
    seq2a = [elm[1] for elm in aligned_seqs]

    # set merit and anchor_list
    # merit = [0] * len(aligned_seqs)
    merit = [''] * len(aligned_seqs)
    ppos1 = 0
    ppos2 = 0
    dummy_seqs = []
    anchor_list = []
    for pos in range(lencc):
        # dummy_seqs += zip_longest_middle(seq1[ppos1:ccmatrixij0[pos][0]], seq2[ppos2:ccmatrixij0[pos][1]], fillvalue='')
        dummy_seqs += zip_longest_middle(seq1[ppos1:ccmatrixij0[pos][0]], seq2[ppos2:ccmatrixij0[pos][1]], fillvalue='')
        ppos1 = ccmatrixij0[pos][0]
        ppos2 = ccmatrixij0[pos][1]
        cpos = len(dummy_seqs)
        merit[cpos] = float("%.2f" % ccmatrixij0[pos][2])
        # if merit[pos]:
            # merit[cpos] = float("%.2f" % ccmatrixij0[pos][2])

        anchor_list += [cpos]

    # dummy_seqs += zip_longest_middle(seq1[ppos1:len1], seq2[ppos2:len2], fillvalue='')
    dummy_seqs += zip_longest_middle(seq1[ppos1:len1], seq2[ppos2:len2], fillvalue='')
    # return seq1a, seq2a, merit

    if seq1a and seq2a and merit:
        assert len(seq1a) == len(seq2a) and len(seq1a) == len(merit)

    out = []
    for elm in zip(seq1a, seq2a, merit):
        out += [list(elm[:])]
    return out

    # return list(zip(seq1a, seq2a, merit))


if __name__ == '__main__':
    main()
