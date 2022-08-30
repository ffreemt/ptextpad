#!/urs/bin/env python
# coding: utf-8
"""
align_sent
"""
import imp
import logging

# based on tryrun_para.py
import os
import pickle  # needed by para_cosine.py
import sys
import time

import numpy as np

try:
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
except ImportError:
    print("[!] You need to install nltk (http://nltk.org/index.html)")

# import vec_cosine
# from vec_cosine import *

# needed by vec_cosine.py
import collections
import math
import re

import jieba
from logzero import logger
from nltk.translate.gale_church import align_blocks

from .get_para import get_enzhfiles

# from seg_ensent import seg_ensent
from .seg_xysent import seg_xysent as seg_ensent  # 080modi
from .seg_zhsent import seg_zhsent

# from detect_language import detect_language

# import blobtr
# imp.reload(blobtr)
# from blobtr import blobtr as glcnpara

#
# files included  para_cosine.py vec_cosine.py glcnpara.py glcn.py
# from para_cosine import para_cosine
# from glcnpara import glcnpara


# import smallseg_rev as smallseg
# import smallseg

# import sseg import SSEG
# jieba = smallseg.SEG()

# from sseg import SSEG
# jieba = SSEG

# needed by glcn
# import requests

# needed by get_response
# from requests.exceptions import ConnectionError

# from para_gc import align_blocks_modi


# from globalst import *  # for gui text_handler setup


def ccmatrix_th(ccmatrix, th0=0.3):
    """
    ccmatrixij = ccmatrix_th(ccmatrix,th0 = 0.3)
    sort out ccmatrix based on a threhold th0
    """
    ccmatrixij0 = []
    # th0 = 0.3
    # jbuffer = -1  # remember the last j value
    j0 = 0
    ibuffer = 0
    len1, len2 = ccmatrix.shape
    for i in range(len1):
        maxv = th0
        jflag = 0  # set to 1 if there exists >=th0
        # jbest = j0+1  # initial jbest
        jp = j0  # previous best j
        for j in range(j0 + 1, len2):
            # select the largest value, if there is a tie, select i,j closer to (i+1,j0+1)
            if ccmatrix[i, j] >= maxv:
                j0a = j  # inital j0
                if (
                    abs(ccmatrix[i, j] - maxv) < 0.02 and jflag
                ):  # if tie, select the j closer to the previous j (j0); the "and jflag" part takes care of the first j run
                    if abs(j - jp - (i - ibuffer) * len2 / len1) > abs(
                        j0 - jp - (i - ibuffer) * len2 / len1
                    ):
                        j0a = j0  # revert to j0, no change
                j0 = j0a
                jflag = 1

                maxv = ccmatrix[i, j]
        if jflag:
            ccmatrixij0 += [[i, j0, ccmatrix[i, j0]]]
            ibuffer = i
    return ccmatrixij0


def align_sent(seq1, seq2, ccmatrixij):
    r"""Do ecsents_batch = align_sent(seq1, seq2, ccmatrixij): en\t\zh."""
    ###
    # generate inbetween cosine sent matrix
    # up to the last entry in ccmatrixij

    known_language = [
        "danish",
        "dutch",
        "english",
        "finnish",
        "french",
        "german",
        "hungarian",
        "italian",
        "norwegian",
        "portuguese",
        "russian",
        "spanish",
        "swedish",
        "turkish",
    ]  # pickle files exist in nltk
    # language = detect_language( ' '.join( seq1[:] )) # unkonw text (to nltk, e.g. chinese, japanese etc.) will be detected as 'english'!  #080modi
    language = "english"

    e0 = 0
    c0 = 0  # initilize, reset at the end of k loop
    ecsents_batch = []

    lencc = len(ccmatrixij)
    if not lencc:
        logger.info(" Align directly with: align_sent_d(seq1,seq2) ==> ecsents_batch")
        ecsents = []
        ecsents += [
            " 1st to be fixed with align_sent_d(seq1,seq2)\t 2nd to be fixed with align_sent_d(seq1,seq2)"
        ]
        ecsents_batch += ecsents
        return ecsents_batch

    logger.info("Aligning sents...total segments:{}".format(lencc))
    # else:
    # logger.info("Since Step 2 is incomplete, the process time can be exceedingly long, and the end results may not be that desirable as well.")

    for k in range(len(ccmatrixij)):
        logger.info("*** {} of {} ".format(k + 1, lencc))
        # up to ccmatrixij[k]
        ij0 = k
        e1 = ccmatrixij[ij0][0]
        c1 = ccmatrixij[ij0][1]  #

        logger.debug(
            "+++++ k:{} ccmatrixij[k]:{} e0:{} c0:{} ".format(k, ccmatrixij[k], e0, c0)
        )

        # additinal text in chinese, e.g., footnotes
        # logger.debug("\n\n kkkkkkkkkkk:{} (1 top)  ccmatrixij[k]:{} e0 {} e1 {} c0 {} c1 {}".format(k,ccmatrixij[k],e0,e1,c0,c1))
        if ((e1 - e0) == 0) and ((c1 - c0) == 0):  # do nothing
            # pass
            logger.debug(" pass ")
            ecsents = []
        elif (e1 - e0) == 0:
            # pass
            ecsents = []
            for csent0 in range(c0, c1):
                ecsents.append("NAdummy\t" + seq2[csent0])
            # logger.debug(" (e1 -e0)==0 ")
            logger.debug(" {} ".format(seq2[csent0]))  # cchange

        elif (c1 - c0) == 0:  # additinal text in english, not translated
            # pass
            ecsents = []
            for csent0 in range(e0, e1):
                ecsents.append(seq1[csent0] + "\tNAdummy")
                # logger.debug(" >>> (c1 -c0)==0 ")
                logger.debug(" {} ".format("NAdummy"))  # cchange
        else:  # { normal process

            # ecmatrix = np.zeros( (e1 -e0,c1 -c0) )
            # collect en sents
            totse = []
            for i0 in range(e0, e1):
                totse += seg_ensent(seq1[i0], language)  # default to english
                # totse += seg_ensent( seq1[i0],language) #080modi

            # collect zh sents
            totsc = []
            for i0 in range(c0, c1):
                totsc += seg_zhsent(seq2[i0])

            logger.debug(">>> totse:{} totsc:{} ".format(totse, totsc))

            if not totsc:  # fix empty totsc( why empty?)
                totsc += ["NAempty"]

            # logger.debug(" totse:{} ".format(totse))
            # logger.debug(" totsc:{} ".format(totsc))

            s1 = [len(totse[i]) for i in range(len(totse))]
            s2 = [len(totsc[i]) for i in range(len(totsc))]

            logger.debug(">>> s1:{} s2:{} ".format(s1, s2))

            lenen = len(s1)
            lenzh = len(s2)

            # print(k)
            # logger.debug("s1:{}  s2:{}".format(s1,s2))
            max1 = max(s1)
            s1a = [s1[i] / max1 * 100 for i in range(len(s1))]
            # s1a = [ s1[i]/10 for i in range( len(s1) )]
            alignvec = align_blocks(s1a, s2)

            logger.debug(">>>> s1a:{}  ".format(s1a))
            logger.debug(">>>alignvec(s1a,s2):{}".format(alignvec))

            # pair = lambda i: [totse[ alignvec[i][0] ], totsc[ alignvec[i][1] ]]
            # [pair(i) for i in range( len(alignvec))]

            #
            logger.debug("> totse:{} totsc:{}".format(totse, totsc))

            # initialize e-c sents pair ecsents
            ecsents = []

            i0 = (
                -1
            )  # tmp var to help collect multiple totsc, e.g., alignvec=[...(2,3),(2,4)... ]
            for vec in alignvec:
                logger.debug("vec>>>> k:{} vec:{}  ".format(k, vec))
                if vec[0] == i0:
                    ecsents[i0] += totsc[vec[1]]
                else:
                    i0 = vec[0]
                    ecsents.append(totse[vec[0]] + "\t" + totsc[vec[1]])
                # print(vec, ecsents)
                logger.debug(" ecsents:{}".format(ecsents))

            logger.debug(
                " ****(normal proc) alignvec:{} len(ecsents):{} ecsents:{}".format(
                    alignvec, len(ecsents), ecsents
                )
            )
        ecsents_batch += ecsents

        e0 = ccmatrixij[k][0]
        c0 = ccmatrixij[k][1]  # }

        #
        # ccmatrixij[k] itself
        ij0 = k
        e1 = ccmatrixij[ij0][0] + 1
        c1 = ccmatrixij[ij0][1] + 1
        # ecmatrix = np.zeros( (e1 -e0,c1 -c0) )
        # collect en sents
        totse = []
        for i0 in range(e0, e1):
            totse += seg_ensent(seq1[i0], language)  # 080modi

        # collect zh sents
        totsc = []
        for i0 in range(c0, c1):
            totsc += seg_zhsent(seq2[i0])

        if not totsc:  # fix empty totsc( why empty?)
            totsc += ["NAempty"]

        # logger.debug(" totsc:{} ".format(totsc)) #cchange

        s1 = [len(totse[i]) for i in range(len(totse))]
        s2 = [len(totsc[i]) for i in range(len(totsc))]

        lenen = len(s1)
        lenzh = len(s2)

        max1 = max(s1)
        s1a = [s1[i] / max1 * 100 for i in range(len(s1))]
        # s1a = [ s1[i]/10 for i in range( len(s1) )]
        alignvec = align_blocks(s1a, s2)

        # pair = lambda i: [totse[ alignvec[i][0] ], totsc[ alignvec[i][1] ]]
        # [pair(i) for i in range( len(alignvec))]

        # initialize e-c sents pair ecsents
        ecsents = []

        logger.debug(" alignvec:{}".format(alignvec))

        i0 = -1  # tmp var to help collect multiple totsc
        for vec in alignvec:
            logger.debug(" vec: {} ".format(vec))
            logger.debug(" i0: {} ecsents:{}".format(i0, ecsents))
            if vec[0] == i0:
                ecsents[i0] += totsc[vec[1]]
            else:
                i0 = vec[0]
                ecsents.append(totse[vec[0]] + "\t" + totsc[vec[1]])
            # print(vec, ecsents)

        # logger.debug(" >>****(k itself) len(ecsents):{},ecsents:{}  ".format( len(ecsents),ecsents ))
        ecsents_batch += ecsents

        e0 = ccmatrixij[k][0] + 1
        c0 = ccmatrixij[k][1] + 1
        # end ccmatrixij last entry

    # ccmatrixij last entry to end
    e1 = len(seq1)
    c1 = len(seq2)

    # nonempty ccmatrixij
    # if 'k' in locals():
    # logger.debug(">k {} e0 {} e1 {} c0 {} c1 {}".format(k,e0,e1,c0,c1))

    if ((e1 - e0) == 0) and ((c1 - c0) == 0):  # do nothing
        pass
        ecsents = []
    elif (e1 - e0) == 0:
        # pass
        ecsents = []
        for csent0 in range(c0, c1):
            ecsents.append("NAdummy\t" + seq2[csent0])

    elif (c1 - c0) == 0:  # additinal text in english, not translated
        # pass
        ecsents = []
        for csent0 in range(e0, e1):
            ecsents.append(seq1[csent0] + "\tNAdummy")
    else:  # { normal process

        # ecmatrix = np.zeros( (e1 -e0,c1 -c0) )
        # collect en sents
        totse = []
        for i0 in range(e0, e1):
            totse += seg_ensent(seq1[i0], language)  # 080modi

        # collect zh sents
        totsc = []
        for i0 in range(c0, c1):
            totsc += seg_zhsent(seq2[i0])

        s1 = [len(totse[i]) for i in range(len(totse))]
        s2 = [len(totsc[i]) for i in range(len(totsc))]

        lenen = len(s1)
        lenzh = len(s2)

        # print(k)
        # logger.debug("ecsents_batch  s1 {}  s2 {} k {}".format(s1,s2,k))
        max1 = max(s1)
        s1a = [s1[i] / max1 * 100 for i in range(len(s1))]
        # s1a = [ s1[i]/10 for i in range( len(s1) )]
        alignvec = align_blocks(s1a, s2)

        # pair = lambda i: [totse[ alignvec[i][0] ], totsc[ alignvec[i][1] ]]
        # [pair(i) for i in range( len(alignvec))]

        # initialize e-c sents pair ecsents
        ecsents = []

        i0 = -1  # tmp var to help collect multiple totsc
        for vec in alignvec:

            if vec[0] == i0:
                ecsents[i0] += totsc[vec[1]]
            else:
                i0 = vec[0]
                ecsents.append(totse[vec[0]] + "\t" + totsc[vec[1]])
            # print(vec, ecsents)
    # }
    ecsents_batch += ecsents

    return ecsents_batch


def save_sents(ecsents_batch, output12, output1, output2, overwrite=False):
    """
    save_sents(ecsents_batch,output12,output1,output2,overwrite=False)
    """
    logger = logging.getLogger(__name__ + "save_sents")
    logger.addHandler(logging.NullHandler())
    # logger.setLevel(logging.DEBUG)

    logger.debug(
        "output12 {} output1 {} output2 {} ".format(output12, output1, output2)
    )

    # ofile = os.path.abspath(ofile)
    # dirname,filename=os.path.split(ofile)
    # fntrunk,fnext = os.path.splitext(filename)

    # outdirname = dirname+'\\aligned\\'
    # os.makedirs(outdirname, exist_ok=True)

    # output12 = os.path.join(outdirname,fntrunk+'_12'+fnext)
    # output1 = os.path.join(outdirname,fntrunk+'_1'+fnext)
    # output2 = os.path.join(outdirname,fntrunk+'_2'+fnext)

    if not overwrite:
        # check if files exist
        if os.path.isfile(output12):
            # raise SystemExit("File "+outfile+" already exists. Delete or rename the file and retry...\n")
            # print("File "+os.path.basename(output12)+" already exists. Delete or rename the file and retry...")
            # print(" File "+output12+" already exists. Delete or rename the file and retry...")
            logger.info(
                " File "
                + output12
                + " already exists. Delete or rename the file and retry..."
            )
            return None

        if os.path.isfile(output1):
            # raise SystemExit("File "+outfile+" already exists. Delete or rename the file and retry...\n")
            # print("File "+os.path.basename(output12)+" already exists. Delete or rename the file and retry...")
            # print(" File "+output1+" already exists. Delete or rename the file and retry...")
            logger.info(
                " File ",
                output1,
                " already exists. Delete or rename the file and retry...",
            )
            return None

        if os.path.isfile(output2):
            # raise SystemExit("File "+outfile+" already exists. Delete or rename the file and retry...\n")
            # print("File "+os.path.basename(output12)+" already exists. Delete or rename the file and retry...")
            # print(" File "+output2+" already exists. Delete or rename the file and retry...")
            logger.info(
                " File ",
                output2,
                " already exists. Delete or rename the file and retry...",
            )
            return None

    # try:
    # f12 = open(output12,'w',encoding='utf8')
    # f1 = open(output1,'w',encoding='utf8')
    # f2 = open(output2,'w',encoding='utf8')
    # for sent in ecsents_batch:
    # f12.write(sent+"\n")
    # s12 = sent.split('\t',1)
    # f1.write(s12[0]+"\n\n") # feature: para #f1.write(s12[0].strip()+"\n\n") # strip to get rid of the space in the line beginning (where is it introduced? seg_ensent?)
    # f2.write(s12[1]+"\n\n")
    # f12.close()
    # f1.close()
    # f2.close()
    # except:
    # logger.error('Something wrong with file reading or writing...')
    with open(output12, "w", encoding="utf8") as f12, open(
        output1, "w", encoding="utf8"
    ) as f1, open(output2, "w", encoding="utf8") as f2:
        for sent in ecsents_batch:
            f12.write(sent + "\n")
            s12 = sent.split("\t", 1)
            # f1.write(s12[0]+"\n\n") # feature: para #f1.write(s12[0].strip()+"\n\n") # strip to get rid of the space in the line beginning (where is it introduced? seg_ensent?)
            if s12[0].strip():
                f1.write(s12[0] + "\n\n")
            else:
                f1.write("NNA\n\n")

            if len(s12) == 2:
                if s12[1].strip():
                    f2.write(s12[1] + "\n\n")
                else:
                    f2.write("NNA\n\n")
            else:
                f2.write("NNA\n\n")
    return None


# para_cosine.py
def para_cosine(seq1, seq2, extra0, lang="chinese"):
    """zh seq1(list of sents), zh seq2(list of sents): return"""

    if not (isinstance(seq1, list) and isinstance(seq1, list)):
        sys.exit(__name__ + ": not list.")

    len1 = len(seq1)
    len2 = len(seq2)
    lendiff = len2 - len1
    ccmatrix = np.zeros((len1, len2))

    # logger.debug(" p c ...")
    # logger.debug(" len1:{} len2{} ".format(len1,len2))

    logger.info(" Total {} to process ".format(len1))
    # logger.info(" estimated time cap: {} min".format(len1*(20*abs(lendiff))*0.05/60))
    for i in range(len1):
        ji = i + lendiff * i / len1
        # print(">>i {}".format(i ))
        logger.info("... {} of {} ".format(i + 1, len1))
        for j in range(len2):
            if abs(j - ji) <= extra0:
                # print("j {}".format(j) )
                # ccmatrix[i, j] = vec_cosine(seq1[i], seq2[j])
                ccmatrix[i, j] = vec_cosine(seq1[i], seq2[j], lang=lang)
                # if ccmatrix[i,j]>0.1:
                # logger.debug("i:{} j:{} {}".format(i,j,ccmatrix[i,j])) #modi
                # logger.debug(" p c i:{} j:{}...".format(i,j))
            # pass
    return ccmatrix


# end of para_cosine.py

# vec_cosine.py
stopstr = "[来你我们在他而了但又和：“”‘’：的，,。 ？]"
stopstr = "[来你我们在他而了但又和：“”‘’：的，,。 ？他她是]"
stopstr = "[来你我们在而了但又和：“”‘’：的，,。 他她是呢]"


def vec_cosine(text1, text2, lang="chinese") -> float:  # consine of text1 and text2
    # stopstr = "[来你我们在他而了但又和：“”‘’：的，,。 ？]"
    # stopstr = "[来你我们在而了但又和：“”‘’：的，,。 ]"

    # check neither text1 or text2 is empty or None
    if not (text1 and text2):
        return 0

    # text1 = re.sub(stopstr, "", text1)
    # text2 = re.sub(stopstr, "", text2)  # done in ztext_to_vector

    len1 = len(text1)
    len2 = len(text2)

    if not (len1 or len2):  # if both zero
        return 0.0

    # add modification factor to consider length discrepancy: rewards same lengths, penelizes different lengths

    # mf = 1.0 - 2 * abs(len1 - len2)/(len1 + len2)  # modi
    # clip = lambda i: i if i>0 else 0
    # a > 3b, or b > 3a, set cosine = 0

    mf = 1.0 - 3 * abs(len1 - len2) / (len1 + len2)
    # a > 2b or b > 2a, set cosine = 0

    mf = max(0, mf)

    if lang == "chinese":
        resu = mf * get_cosine(ztext_to_vector(text1), ztext_to_vector(text2))
    else:
        # resu = mf*get_cosine(collections.Counter(wordpunct_tokenize(text1)), collections.Counter(wordpunct_tokenize(text2)))  # latine lang: text_to_vector  # noqa
        resu = mf * get_cosine(
            text_to_vector(text1), text_to_vector(text2)
        )  # latine lang: text_to_vector  # noqa

    return resu

    # return mf*get_cosine(ztext_to_vector(text1), ztext_to_vector(text2))
    # modi 2015 10 13


def vec_cosine_a(
    text1, text2, lang="chinese", mf=None
) -> float:  # consine of text1 and text2
    # stopstr = "[来你我们在他而了但又和：“”‘’：的，,。 ？]"
    # stopstr = "[来你我们在而了但又和：“”‘’：的，,。 ]"

    # check neither text1 or text2 is empty or None
    if not (text1 and text2):
        return 0

    # text1 = re.sub(stopstr, "", text1)
    # text2 = re.sub(stopstr, "", text2)  # done in ztext_to_vector

    len1 = len(text1)
    len2 = len(text2)

    if not (len1 or len2):  # if both zero
        return 0.0

    # add modification factor to consider length discrepancy: rewards same lengths, penelizes different lengths

    # mf = 1.0 - 2 * abs(len1 - len2)/(len1 + len2)  # modi
    # clip = lambda i: i if i>0 else 0
    # a > 3b, or b > 3a, set cosine = 0

    if mf is None:
        mf = 1.0 - 3 * abs(len1 - len2) / (len1 + len2)
        # a > 2b or b > 2a, set cosine = 0

        mf = max(0, mf)
    else:
        mf = 1

    if lang == "chinese":
        resu = mf * get_cosine(ztext_to_vector(text1), ztext_to_vector(text2))
    else:
        # resu = mf*get_cosine(collections.Counter(wordpunct_tokenize(text1)), collections.Counter(wordpunct_tokenize(text2)))  # latine lang: text_to_vector  # noqa
        resu = mf * get_cosine(
            text_to_vector(text1), text_to_vector(text2)
        )  # latine lang: text_to_vector  # noqa

    return resu

    # return mf*get_cosine(ztext_to_vector(text1), ztext_to_vector(text2))
    # modi 2015 10 13


def text_to_vector(
    text, lang="english"
):  # may need to branch for other asian languages
    import string

    # words = text.split()
    # refer to detect_language.py
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # stopwords.fileids():
    # lang_set = ['danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'norwegian', 'portuguese', 'russian', 'spanish', 'swedish', 'turkish']

    # lang = lang if lang in lang_set else 'english'
    # for elm in stopwords.words(lang):
    # if elm in words:
    # words.remove(elm)

    counter0 = collections.Counter(words)

    # remove punctuations
    for elm in string.punctuation:
        if elm in counter0.keys():
            # print(elm)
            counter0.pop(elm)

    return counter0


def ztext_to_vector(text):
    # import smallseg

    # words = WORD.findall(text)
    # words = [s for s in jieba.cut(text,True)]
    # text1 = re.sub("[的，,]","",text1)

    # text = re.sub(stopstr, "", text)  # for the original jieba.cut

    # text = re.sub(stopstr, " ", text)  # SEG.cut
    def pre_process(text):
        for elm in "来你我们在而了但又和的他她是呢":
            # if elm in text:            print(elm)
            text = text.replace(elm, " ")
        return text

    text = pre_process(text)

    # words = [s for s in jieba.cut(text)]
    # return collections.Counter(words)

    return collections.Counter(jieba.cut(text))


def get_cosine(vec1, vec2):
    log = logging.getLogger(__name__ + ":get_cosine")
    log.addHandler(logging.NullHandler())
    # log.setLevel(logging.INFO)
    # log.setLevel(logging.DEBUG)
    # log.debug("get_cosine starting...")
    intersection = set(vec1.keys()) & set(vec2.keys())

    # modified #2015 11 09
    # if # of common terms is smaller than 4， set cosine to 0
    if len(intersection) < 5:
        return 0.0

    # log.debug(" intersection={intersection} ".format(intersection=intersection))
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return round(float(numerator) / denominator, 2)


# end of vec_cosine.py

if __name__ == "__main__":
    enfile = "26-40-en.txt"
    zhfile = "26-40-zh.txt"

    # enfile = '13-25-en.txt'
    # zhfile = '13-25-zh.txt'

    enfile = "newsen.txt"
    zhfile = "newszh.txt"

    eninfile = "D:\\dl\\Dropbox\\shuangyu_ku\\txt-books\\复活\\" + enfile
    zhinfile = "D:\\dl\\Dropbox\\shuangyu_ku\\txt-books\\复活\\" + zhfile

    seq1, ll1, seq2, ll2 = get_enzhfiles(eninfile, zhinfile)

    # seqgl = list( map(lambda enseq:glcnpara(enseq) ,seq1))
    # print(' gl.cn time used {} '.format( time.clock()-t0 ))

    filenametrunk = os.path.splitext(enfile)[0][:-3]
    seqglfile = "seqgl" + os.path.splitext(enfile)[0][:-3] + ".pickle"

    if os.path.exists("picklefiles\\" + seqglfile):
        # if os.path.exists(seqglfile):
        seqgl = pickle.load(open("picklefiles\\" + seqglfile, "rb"))
    else:
        t0 = time.clock()
        print(" gl.cn {} ".format(t0), flush=True)
        seqgl = list(map(lambda enseq: glcnpara(enseq), seq1))
        print(" gl.cn time used {} ".format(time.clock() - t0))
        os.makedirs("picklefiles", exist_ok=True)
        pickle.dump(seqgl, open("picklefiles\\" + seqglfile, "wb"))

    t0 = time.clock()
    print(" calculate ccmatrix... ")
    extra0 = 10
    ccmatrix = para_cosine(seqgl, seq2, extra0)
    print(" ccmatrix time used {} ".format(time.clock() - t0))

    len1 = len(ll1)
    len2 = len(ll2)
    th0 = 0.3

    ccmatrixij0 = ccmatrix_th(ccmatrix)
    # logger.info(" ccmatrixij0 at line 408")
