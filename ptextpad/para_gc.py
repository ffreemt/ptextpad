# import os, sys, logging, imp, time
import logging
import os
import sys

import numpy as np
from nltk.translate.gale_church import align_blocks

# from vec_cosine import *
from .get_para import (  # get_para(filename, linesep='')->"seqlist, lenlist" get_enzhfiles(filename1, filename2)->"seq1, ll1, seq2, ll2"
    get_enzhfiles,
    get_para,
)

# from .amend_avec import amend_avec


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _test():  # inter fucntion, cant call para_gc._test
    """
    copy and paste to ipython, then run _test()
    import doctest; doctest.testmod( module name)

    or in ipython
    %run file.py

    or
    if __name__ == "__main__":
        _test()
    and run py file.py
    """
    import doctest

    doctest.testmod()


def align_blocks_0(source_sents, target_sents) -> str:
    """
    alignvec = align_blocks_0(source_sents, target_sents)
    return align_blocks(source_sents, target_sents)
    or None
    """
    try:
        return align_blocks(source_sents, target_sents)
    except Exception:
        return None


def combine_len(ll1, i0) -> (str, str):
    """Gen.

    ll1a, i0, delta = combine_len(i0, ll1)
    combine ll1[i0] to ll1[ i0 -1 mod len(ll1)  ], 0<=i0<len(ll1), do nothing otherwise
    combine ll2[j0] to ll1[ j0 -1 mod len(ll2)  ], 0<=j0<len(ll1) do nothing otherwise
    """
    logger = logging.getLogger(__name__ + ".combine_len")
    logger.addHandler(logging.NullHandler())
    # logger.setLevel(logging.DEBUG)

    len1 = len(ll1)
    ll1a = [el for el in ll1]  # make a copy

    if len1 == 1:  # len1=1 nothing to do
        logger.warning(" len1 = 1, nothing to do. ")
        return ll1, -1, 0  # invalid i0 to prevent future decombine
    else:
        if i0 == 0:
            delta = ll1a[i0]
            ll1a[i0 + 1] += delta  # prepare

            ll1a = ll1a[i0 + 1 :]  # slicing 1:len1

        elif i0 > 0 and i0 < len1:
            # pass
            delta = ll1a[i0]
            ll1a[i0 - 1] += delta  # prepare
            ll1a = ll1a[:i0] + ll1a[i0 + 1 :]  # slicing
        else:
            logger.warning("i0:{} out of range.".format(i0))
            # delta = -1
            return None
        return ll1a, i0, delta


def decombine_len(ll1a, i0, delta) -> str:
    """Gen.

    ll1 = decombine_len(i0, delta, ll1a)
    """
    logger = logging.getLogger(__name__ + ".decombine_len")
    logger.addHandler(logging.NullHandler())
    # logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.INFO)

    len1a = len(ll1a)  # len1a = len1 -1
    ll1 = [el for el in ll1a]
    logger.debug(" ll1:{}".format(ll1))
    if i0 == 0:
        ll1[i0] -= delta

        ll1 = [delta] + ll1
        logger.debug(" ll1:{}".format(ll1))
    elif i0 > 0 and i0 <= len1a:

        ll1[i0 - 1] -= delta
        logger.debug(" ll1:{}".format(ll1))
        ll1 = ll1[:i0] + [delta] + ll1[i0:]
        logger.debug(" ll1:{}".format(ll1))
    else:
        logger.warning("i0:{} invalid input.".format(i0))
        return None

    return ll1


def recover_avec(avec0, col=0, pos=0) -> str:
    """Gen.

    avec1 = recover_avec(avec, col=0, pos=0)

    >>> avec1 = [(0, 0), (0, 1), (0, 2), (1, 3), (2, 4)]
    >>> recover_avec(avec1, pos=1)
    [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (2, 3), (3, 4)]

    >>> avec = [(0, 3), (0, 4), (1, 5), (1, 6), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12), (6, 11), (6, 12), (7, 13), (7, 14)]
    >>> recover_avec(avec)
    [(0, 3), (1, 3), (0, 4), (1, 4), (2, 5), (2, 6), (3, 5), (3, 6), (4, 7), (4, 8), (5, 9), (5, 10), (6, 11), (6, 12), (7, 11), (7, 12), (8, 13), (8, 14)]
    >>> avec1 = [(0, 0), (1, 1), (2, 2)]
    >>> recover_avec(avec1)
    [(0, 0), (1, 0), (2, 1), (3, 2)]

    """
    # import numpy as py

    logger = logging.getLogger(__name__ + ".recover_avec")
    logger.addHandler(logging.NullHandler())
    # logger.setLevel(logging.DEBUG)

    logger.debug("input: avec0={}, col={}, pos={} ".format(avec0, col, pos))

    if not (col == 0 or col == 1):  # col must be 0 or 1
        logger.warning("col={} invalid input.".format(col))
        return None

    # set col
    colx = (col + 1) % 2  # set the other column

    listo = [el[col] for el in avec0]
    listx = [el[colx] for el in avec0]
    logger.debug(" listo={} listx={}".format(listo, listx))

    # grow two lists based on listo and listx; zip the two lists in the end
    listo1 = []
    listx1 = []
    if pos == 0:
        # for all i>pos: ;(i, x)=>(i+1, x)
        for el in avec0:
            if el[col] == pos:  # expand to two terms
                listo1 += [el[col], el[col] + 1]
                listx1 += [el[colx], el[colx]]
            else:  # increase by one
                listo1 += [el[col] + 1]
                listx1 += [el[colx]]
    else:  # pos>=1
        for el in avec0:
            logger.debug("el={} listo={} listx={}".format(el, listo, listx))
            if el[col] < (pos - 1):
                listo1 += [el[col]]
                listx1 += [el[colx]]
            elif el[col] == (pos - 1):  # expan to two terms
                listo1 += [el[col], el[col] + 1]
                listx1 += [el[colx], el[colx]]
            else:  # increase by one
                listo1 += [el[col] + 1]
                listx1 += [el[colx]]
            logger.debug("==> el={} listo={} listx={}".format(el, listo, listx))
    # zip two lists
    if col == 0:
        avec1 = list(zip(listo1, listx1))
    else:
        avec1 = list(zip(listx1, listo1))

    logger.debug("output avec1={}".format(avec1))
    # avec_nparray = np.array( avec ).transpose()[pos] # convert to array/list
    # avec_nparray0 = np.copy( avec_nparray ) # make a copy

    # if pos==0:
    # pass
    # elif pos>0 and pos<:

    # avec1 = avec
    return avec1


# moved to align_blocks_final.py to avoid circular import of amend_avec


# {
def align_blocks_modi(source_sents, target_sents) -> str:
    """Align vec = align_blocks_modi(source_sents, target_sents)
    modified align_blocks."""
    logger = logging.getLogger("align_blocks_modi")
    # logger = logging.getLogger(__name__+".align_blocks_modi")
    logger.addHandler(logging.NullHandler())
    # logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.WARNING)

    if not (source_sents and target_sents):
        logger.warning(" Input is empty. Exiting...")
        return None

    # attemp without modification
    avec = align_blocks_0(source_sents, target_sents)
    if avec is not None:  # success
        logger.debug("Success without modi.")
        return avec

    # it not successful, proceed
    ll1, ll2 = source_sents, target_sents

    max1 = max(ll1)
    min1 = min(ll1)
    max2 = max(ll2)
    min2 = min(ll2)

    sum1 = sum(ll1)
    sum2 = sum(ll2)

    mean1 = np.mean(ll1)
    mean2 = np.mean(ll2)

    # set mean to be the smaller of the two
    if mean1 < mean2:
        ll2a = [el * mean1 / mean2 for el in ll2]
        avec = align_blocks_0(ll1, ll2a)
    else:
        ll1a = [el * mean2 / mean1 for el in ll1]
        avec = align_blocks_0(ll1a, ll2)

    # if not succfull, try to normalize with sum
    if avec is not None:
        logger.debug("Normalized with min mean.")
        # print('Normalized with min mean.')
        return avec
    else:
        logger.debug("normal min mean failed, trying norm min sum.")
        # print('normal min mean failed, trying norm min sum.')
        if sum1 < sum2:
            ll2a = [el * sum1 / sum2 for el in ll2]
            return align_blocks_0(ll1, ll2a)
        else:
            ll1a = [el * sum2 / sum1 for el in ll1]
            return align_blocks_0(ll1a, ll2)


# } end of align_blocks_modi

# max0 = 100
# min0 = 10

# alignvec = None
# try:
# logger.debug(" 1a try ")
# alignvec = align_blocks(ll1, ll2)
# except:
# try:
# len1sum = sum(ll1)
# len2sum = sum(ll2)
# ll1a =  [ ll*len2sum/len1sum for ll in ll1] # total length the same
# logger.debug(" 1b try")
# alignvec = align_blocks(ll1a, ll2)
# except:
# try:
# ll1a = [ ll/max1*max0 for ll in ll1] # limit max to max0=100
# logger.debug(" 2nd try")
# alignvec = align_blocks(ll1a, ll2)
# except:
# try:
# ll1a = [ ll/min1*min0 for ll in ll1] #set min = min0(10)
# logger.debug(" 3rd try")
# alignvec = align_blocks(ll1a, ll2)
# except:
# logger.error(" Unable to align.")
# return alignvec


def check_avec(avec1, max0=-1, max1=-1) -> (str, str):
    """
    missing0, missing1=check_avec(avec1)
    check missing positions in align vector

    >>> avec1 = [(0, 1), (0, 2), (1, 1), (1, 2)]
    >>> check_avec(avec1)
    ([], [0])
    >>> avec1 = [(0, 0), (0, 2), (1, 1), (1, 2)]
    >>> check_avec(avec1)
    ([], [])
    """
    logger = logging.getLogger(__name__ + ".check_avec")
    logger.addHandler(logging.NullHandler())
    # logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.WARNING)

    # check all entries has index >=1
    if not isinstance(avec1, list):
        logger.error("Input not a list.")
        return None
    for el in avec1:
        if not (isinstance(el, list) or isinstance(el, tuple)):
            logger.error("At least of the list elments is invalid.")
            return None

    check = True
    for el in avec1:
        if len(el) < 2:
            check = False
    if not check:
        logger.error("One of the elements has length smaller than 2. Exiting...")
        return None

    list0 = [el[0] for el in avec1]
    list1 = [el[1] for el in avec1]
    # missing0 = [el for el in range(max(list0)+1) if el not in list0 ]
    # missing1 = [el for el in range(max(list1)+1) if el not in list1 ]
    if max0 == -1:
        threshold0 = max(list0) + 1
    else:
        threshold0 = max0 + 1
    if max1 == -1:
        threshold1 = max(list1) + 1
    else:
        threshold1 = max1 + 1

    missing0 = [el for el in range(threshold0) if el not in list0]
    missing1 = [el for el in range(threshold1) if el not in list1]
    return missing0, missing1


def para_gc(file1, file2) -> str:
    """Align vec = para_gc(file1, file2)."""
    logger = logging.getLogger(__name__ + ".para_gc")
    logger.addHandler(logging.NullHandler())
    # logger.setLevel(logging.DEBUG)

    if not (os.path.exists(file1) and os.path.exists(file2)):
        logger.error("One of the file or both do not exist. Exiting...")
        # return 1
    else:
        print(True)

    seq1, ll1, seq2, ll2 = get_enzhfiles(file1, file2)

    alignvec = align_blocks_modi(ll1, ll2)

    return alignvec


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,  # for root logger only?
        # level=logging.ERROR,
        format="%(filename)s[line:%(lineno)d] %(name)s %(levelname)s %(message)s",
    )
    logger = logging.getLogger()
    # logger.setLevel(logging.INFO)

    # logger.setLevel(logging.DEBUG)
    _test()
    sys.exit()

    file1 = "newsen.txt"
    file2 = "newszh.txt"

    file1 = "reporten.txt"
    file2 = "reportzh.txt"
    # alignvec1 = para_gc(file1, file2)

    # file1 = r'F:\muecalign\testdata\sternstunden12-de.txt'
    # file2 = r'F:\muecalign\testdata\sternstunden12-zh.txt'
    # seq1, ll1, seq2, ll2 = get_enzhfiles(file1, file2)
    # alignvec2 = para_gc(file1, file2)

    # sys.exit()

    # file1 = 'pt2-21-40-en.txt'
    # file2 = 'pt2-21-40-zh.txt'

    file1 = r"F:\muecalign\testdata\Alices Adventures in Wonderland7-12.txt"
    file2 = r"F:\muecalign\testdata\爱丽丝梦游仙境 阿丽思漫游奇境记赵元任译7-12.txt"

    # file1 = r"F:\muecalign\testdata\alice07-09en.txt"
    # file2 = r"F:\muecalign\testdata\alice07-09zh.txt"

    # file1 = r"F:\muecalign\testdata\alice08-09en.txt"
    # file2 = r"F:\muecalign\testdata\alice08-09zh.txt"

    # file1 = r"F:\muecalign\testdata\alice07en.txt"
    # file2 = r"F:\muecalign\testdata\alice07zh.txt"

    # file1 = r"F:\muecalign\testdata\reporten.txt"
    # file2 = r"F:\muecalign\testdata\reportzh.txt"

    # file1 = r"D:\dl\Dropbox\shuangyu_ku\chinese\Story_of_Stone_Hawkes\hlm-en-01.txt"
    # file2 = r"D:\dl\Dropbox\shuangyu_ku\chinese\Story_of_Stone_Hawkes\hlm-zh-nc-01.txt"

    # file1 = r"D:\dl\Dropbox\shuangyu_ku\txt-books\shawshank\shawshank-en.txt"
    # file2 = r"D:\dl\Dropbox\shuangyu_ku\txt-books\shawshank\shawshank-zh.txt"

    # file1 = r"D:\dl\Dropbox\shuangyu_ku\econ-txt\out1c-en.txt"
    # file2 = r"D:\dl\Dropbox\shuangyu_ku\econ-txt\out1c-zh.txt"

    # file1 = r"D:\dl\Dropbox\shuangyu_ku\txt-books\WhyNationsFail\WhyNationsFail1-en.txt"
    # file2 = r"D:\dl\Dropbox\shuangyu_ku\txt-books\WhyNationsFail\WhyNationsFail1-zh.txt"

    # file1 = r"D:\dl\Dropbox\shuangyu_ku\txt-books\WhyNationsFail\WhyNationsFail1a-en.txt"
    # file2 = r"D:\dl\Dropbox\shuangyu_ku\txt-books\WhyNationsFail\WhyNationsFail1a-zh.txt"

    seq1, ll1 = get_para(file1, linesep=" ", paramode=1)
    seq2, ll2 = get_para(file2, paramode=1)

    # if os.path.exists(file1) and os.path.exists(file2):
    # seq1, ll1, seq2, ll2 = get_enzhfiles(file1, file2)
    # if len(ll1)==1 and len(ll2)==1:
    # seq1, ll1 = get_para(file1, linesep=' ', paramode=1)
    # seq2, ll2 = get_para(file2, paramode=1)

    # else:
    # logger.error(" files not exists")
    # sys.exit()

    # time0 = time.clock(); avec = align_blocks_modi(ll1, ll2); print( not avec is None); time0 = time.clock() - time0; print("time0={}".format(time0))
    # if avec:
    # time1 = time.clock(); ccvec = [ vec_cosine( glcnpara( seq1[ avec[i][0] ]), seq2[avec[i][1]] ) for i in range( len(avec) ) ];time1 = time.clock() - time1; print("time0={}".format(time1))

    # ccveci = [ [i, ccvec[i]] for i in range( len(ccvec) )]

    # ccvec0 = [ [i, ccvec[i]] for i in range(len(ccvec)) if ccvec[i]>0]
    # cout = lambda i: (seq1[ avec[i][0] ], seq2[ avec[i][1] ])

    # ccvec01 = [ [i, ccvec[i]] for i in range(len(ccvec)) if ccvec[i]>0.1 and ccvec[i]<0.2]
    # cout01 = lambda i: (seq1[ avec[ ccvec01[i][0]  ][0] ], seq2[ avec[ ccvec01[i][0]  ][1] ])

    # [[ccveci[i], cout(i)] for i in range( len(ccveci) )  ]

    # t0 = time.clock(); avec = align_blocks_modi(ll1, ll2); print(' Success:', not avec is None); print(time.clock()-t0)
    # cvec = check_avec(avec) ; print(cvec)

    # t0 = time.clock(); avec1 = align_blocks_modi(ll1[:i0], ll2[:j0]); print( avec1 is None); print(time.clock()-t0)
