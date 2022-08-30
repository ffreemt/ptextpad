# coding: utf8
"""
para cosine
"""
import logging
import os
import sys
import time

import numpy as np

from .logging_progress import logging_progress
from .vec_cosine import vec_cosine

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def para_cosine(seq1, seq2, extra0, lang="chinese"):
    """zh seq1(list of sents), zh seq2(list of sents): return"""

    if not (isinstance(seq1, list) and isinstance(seq1, list)):
        sys.exit(__name__ + ": not list.")

    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
    )

    # LOGGER.addHandler(text_handler)  # gui handle (setup in globalst.py (scrolltext))

    len1 = len(seq1)
    len2 = len(seq2)
    lendiff = len2 - len1
    ccmatrix = np.zeros((len1, len2))

    # LOGGER.debug(" p c ...")
    # LOGGER.debug(" len1:{} len2{} ".format(len1,len2))

    # LOGGER.info(" Total {} to process ".format(len1))
    # LOGGER.info(" estimated time cap: {} min".format(len1*(20*abs(lendiff))*0.05/60))
    for i in range(len1):
        ji = i + lendiff * i / len1

        # LOGGER.info("... {} of {} ".format(i+1, len1))
        logging_progress(i, len1, bar_length=30)

        for j in range(len2):
            if abs(j - ji) <= extra0:
                ccmatrix[i, j] = vec_cosine(seq1[i], seq2[j], lang=lang)

    LOGGER.debug("^ ^")
    return ccmatrix

    _ = r"""
    file1 = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\files_for_testing_load\Folding_Beijing_ch1-zh.txt'  # noqa
    file2 = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\files_for_testing_load\Folding_Beijing_ch1-en.txt'  # noqa

    text1 = load_text(file1)
    text2 = load_text(file2)

    seq1 = text_to_paras(text1)
    seq2 = text_to_paras(text2)
    seqgl = []
    lenseq1 = len(seq1)

    tgtlang = detect_lang(text2[:2000])
    # modi 2017 02 09
    seqgl = youdao_tr_list(seq1)

    extra0 = min(10, abs(len(seq1) - len(seq2)))

    # ccmatrix = para_cosine(seqgl, seq2, extra0, tgt)
    ccmatrix = para_cosine(seqgl, seq2, extra0, tgtlang)  # modi noqa
    LOGGER.debug(" **possbile crash point? ** ")

    ccmatrixij0 = ccmatrix_th(ccmatrix)
"""


def main():
    """main."""

    import pickle

    from get_para import get_enzhfiles
    from glcnpara import glcnpara
    from youdao_tr_list import youdao_tr_list

    enfile = "26-40-en.txt"
    zhfile = "26-40-zh.txt"

    enfile = "13-25-en.txt"
    zhfile = "13-25-zh.txt"

    eninfile = "D:\\dl\\Dropbox\\shuangyu_ku\\txt-books\\复活\\" + enfile
    zhinfile = "D:\\dl\\Dropbox\\shuangyu_ku\\txt-books\\复活\\" + zhfile

    seq1, ll1, seq2, ll2 = get_enzhfiles(eninfile, zhinfile)

    seqgl = list(map(lambda enseq: glcnpara(enseq), seq1))
    # print(' gl.cn time used {} '.format( time.clock()-t0 ))

    """
    filenametrunk = os.path.splitext(enfile)[0][:-3]

    seqglfile = 'seqgl' + os.path.splitext(enfile)[0][:-3] + '.pickle'
    # if os.path.exists(seqglfile):
    if os.path.exists('pt1/' + seqglfile):
        seqgl = pickle.load(open('pt1/'+seqglfile, 'rb'))
    else:
        t0 = time.clock()
        print(" gl.cn {} ".format(t0), flush=True)

        # seqgl = list(map(lambda enseq: glcnpara(enseq), seq1))  # modi transalte core step
        seqgl = youdao_tr_list(seq1)

        print(' gl.cn time used {} '.format(time.clock() - t0))
        pickle.dump(seqgl, open('pt1/' + seqglfile, 'wb'))
    """

    t0 = time.clock()
    print(" calculate ccmatrix... ")
    extra0 = 10
    ccmatrix = para_cosine(seqgl, seq2, extra0)
    print(" ccmatrix time used {} ".format(time.clock() - t0))

    len1 = len(ll1)
    len2 = len(ll2)
    len1 = ccmatrix.shape[0]
    len2 = ccmatrix.shape[1]

    th0 = 0.3
    ccmatrixij = [
        [i, j, ccmatrix[i, j]]
        for i in range(len1)
        for j in range(len2)
        if ccmatrix[i, j] > th0
    ]

    # np.savetxt('pt1/' + filenametrunk + 'ij.aligned.txt', np.array(ccmatrixij), '%5.2f')

    sys.exit()

    seqgl = youdao_tr_list(seq2)
    extra0 = 10
    ccmatrix = para_cosine(seqgl, seq1, extra0, "en")
    len1 = ccmatrix.shape[0]
    len2 = ccmatrix.shape[1]

    th0 = 0.3
    ccmatrixij = [
        [i, j, ccmatrix[i, j]]
        for i in range(len1)
        for j in range(len2)
        if ccmatrix[i, j] > th0
    ]

    # test data
    eninfile = r"D:\dl\Dropbox\mat-dir\python-zh-mat\para_align_ratio\pt2-01-20-en.txt"
    zhinfile = r"D:\dl\Dropbox\mat-dir\python-zh-mat\para_align_ratio\pt2-01-20-en.txt"

    eninfile = "D:\\dl\\Dropbox\\shuangyu_ku\\txt-books\\复活\\13-25-en.txt"
    zhinfile = "D:\\dl\\Dropbox\\shuangyu_ku\\txt-books\\复活\\13-25-zh.txt"

    seq1, ll1, seq2, ll2 = get_enzhfiles(eninfile, zhinfile)
    # get_para(infile)
    # from D:\dl\Dropbox\mat-dir\python-zh-mat\para_cosine
    # list
    # seqgl[i] = glcnpara(seq1[i])

    ###########
    # seqgl = list( map(lambda enseq:glcnpara(enseq) ,seq1) )
    # pickle.dump(seqgl,open('seqglpt2ch01-ch20.pickle','wb'))
    # pickle.load(open("seqglpt2ch01-ch20.pickle", "rb"))

    ########
    extra0 = 10
    ccmatrix = para_cosine(seqgl, seq2, extra0)

    len1 = len(ll1)
    len2 = len(ll2)
    th0 = 0.3
    ccmatrixij = [
        [i, j, ccmatrix[i, j]]
        for i in range(len1)
        for j in range(len2)
        if ccmatrix[i, j] > th0
    ]

    # cout = lambda i,j: [seq1[i],seq2[j]]
    # cout2 = lambda ij: [seq1[ ccmatrixij[ij][0] ],seq2[ccmatrixij[ij][1]]]

    # np.savetxt( 'c0.txt',np.array(ccmatrixij), '%5.2f' )
    # c0 = np.array(ccmatrixij)
    # np.savetxt( 'c0.txt',c0, '%5.2f' )

    # [[ccmatrixij[i],cout2(i)] for i in range(30,40)]

    # ccmatrixijs = [[i,j,ccmatrix[i,j],cout(i,j)] for i in range(len1) for j in range(len2) if ccmatrix[i,j]>th0 ]

    # len(  seq1[int( ccnp[i,0] )] )/ len(  seq2[int( ccnp[i,1] )] )
    # lenratio = lambda i: (len(  seq1[int( ccnp[i,0] )] )/ len(  seq2[int( ccnp[i,1] )] ))
    # lenratio0 = sum( [lenratio(i) for i in range( ccnp.shape[0]  ) ])/ccnp.shape[0]


if __name__ == "__main__":
    main()
