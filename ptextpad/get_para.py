'''Get paras and para lengths.'''
import os
import sys
import logging
import re  # for removing '\u3000'
# import imp

# import numpy  #numpy.zeros((5, 5))
# or matrix = [[0 for i in range(5)] for j in range(5)]

# import glcn
# imp.reload(glcn)
# from glcn import glcn
# from glcnweb import glcnweb

# modname = "vec_cosine"
# import vec_cosine
# imp.reload(vec_cosine)
# from vec_cosine import vec_cosine


# import pick_ij
# imp.reload(pick_ij)
# from pick_ij import pick_ij

# import joint_par
# imp.reload(joint_par)
# from joint_par import joint_par

def get_para(filename, linesep='', paramode=0, encoding='utf8'):  # ->"seqlist,lenlist":
    '''seqlist,lenlist=get_para(filename,linesep='',paramod=0,encoding='utf8'):

    blank lines separate paragraphs (paramode = 0)
    linesetp (default to empty ('')) should
    be set to space (' ') for english, empty ('') for chinese text.

    paramode = 0 (default): blank separates para, NewLINE IS NOT a new para
    paramode = 1: newline, each line IS a new para
    '''
    # with open(filename,"r",encoding="utf-8") as f:
    # with open(filename,"r",encoding=encoding) as f:
    with open(filename, "rb") as f:
        seqlist = []
        lenlist = []

        if paramode == 0:
            nonblank = False
            seq0 = ""
            blanknumb = 1  # fixed ##take care of initial empty lines; prepare
            # for #xxx
            for line in f:
                # line = line.decode("utf-8","ignore")
                line = line.decode(encoding, "ignore")
                line = re.sub('\u3000', '', line)  # modi

                # nonblank; strip(' \r\n') to retain \t
                if len(line.strip(' \r\n')):
                    # new en para starts with a space
                    seq0 += linesep + line.strip(' \r\n')
                    blanknumb = 0
                else:  # blank
                    blanknumb += 1  # revised
                    # xxx first blank line after nonblank line; flush out
                    if blanknumb == 1:
                        seqlist.append(seq0)
                        lenlist.append(len(seq0))
                        seq0 = ""

            # process last line not blank; flush out
            if seq0:
                seqlist.append(seq0)
                lenlist.append(len(seq0))
        else:  # mode 1: newline a para
            for line in f:
                # line = line.decode("utf-8","ignore")
                line = line.decode(encoding, "ignore")
                line = re.sub('\u3000', '', line)  # modi

                if len(line.strip(' \r\n')):   # non blank
                    #  new en para starts with a space
                    seq0 = linesep + line.strip(' \r\n')
                    seqlist.append(seq0)
                    lenlist.append(len(seq0))
    return seqlist, lenlist


# "seq1,ll1,seq2,ll2"
def get_enzhfiles(filename1, filename2):
    # imp.reload(logging)

    # log = logging.getLogger(__name__)

    log = logging.getLogger("get_enzhfiles")
    log.addHandler(logging.NullHandler())

    # logging.getLogger('foo').addHandler(logging.NullHandler())

    # log.setLevel(logging.DEBUG)
    log.setLevel(logging.INFO)

# filename=LOG_FILENAME,
# filemode='w'

    # filename1 = "pt2-41-42-en.txt"
    # filename2 = "pt2-41-42-zh.txt"

    # filename1 = "pt2-01-20-en.txt"
    # filename2 = "pt2-01-20-zh.txt"

    # filename1 = "pt2-01-20-en1.txt"
    # filename2 = "pt2-01-20-zh1.txt"

    log.debug("reading in files")
    seq1, ll1 = get_para(filename1, linesep=' ')
    seq2, ll2 = get_para(filename2)
    len1 = len(ll1)
    len2 = len(ll2)
    # log.info("Exiting ...")
    # raise SystemExit("Testing SystemExit...")
    # return seq1,ll1,seq2,ll2,len1,len2
    return seq1, ll1, seq2, ll2

    # i10,i20,merit0 = slide_match.slide_match(ll1,ll2)

# align_chunk(seq1,ll1,seq2,ll2,clen,extra0,pc0th,pc1th):
# pick_ij(pcmatrix)


if __name__ == "__main__":
    import importlib
    importlib.reload(logging)  # needed in ipython
    # level=logging.DEBUG,  # for root logger only?
    # level=logging.ERROR,
    logging.basicConfig(format='%(filename)s[line:%(lineno)d] %(name)s %(levelname)s %(message)s',)

    # seq1,ll1,seq2,ll2,len1,len2 = main()

    # filename1 = "pt2-01-20-en.txt"
    # filename2 = "pt2-01-20-en.txt"
    eninfile = r"D:\dl\Dropbox\mat-dir\python-zh-mat\para_align_ratio\pt2-01-20-en.txt"
    zhinfile = r"D:\dl\Dropbox\mat-dir\python-zh-mat\para_align_ratio\pt2-01-20-zh.txt"

    # filename1 = "pt2-41-42-en.txt"
    # filename2 = "pt2-41-42-zh.txt"

    seq1, ll1, seq2, ll2 = get_enzhfiles(eninfile, zhinfile)

    # inp0 = seq1,ll1,seq2,ll2,clen,extra0,pc0th,pc1th
    # pcmatrix,pcmatrixp,pcmatrix01,pcmatrix0r,pcmatrix0p = align_chunk(seq1,ll1,seq2,ll2,clen,extra0,pc0th,pc1th)

    outfile = 'ch1ch20par_aligned1.txt'
    outfile = 'ch41ch42par_aligned1.txt'
    outfile = 'outfile.txt'
    # outfile = '-'.join( os.path.splitext(filename1)[0].split('-')[:3] )+'par_aligned_clen{clen}sumijth{sumijth}.txt'.format(clen=clen,sumijth=sumijth)
    # for filename1 = = "pt2-01-20-en.txt",
    # outfile =  'pt2-01-20_aligned_clen20sumijth12.0.txt'

    # run joint_par.py
    # joint_par(seq1,seq2,outij,outfile)

    # numpy.set_printoptions(threshold=numpy.inf)
    # store pcmatrix > pcmatrix.txt
    # file:///D:\dl\Dropbox\mat-dir\python-zh-mat\para_align\pearson calculation.py
    # look for alignment points based on pearson's correlation

    sys.exit()

    # glcnpar = lambda x: map(glcn, x)  # works ok, but need to work with iterator
    i1 = 16
    i2 = 26

    i1 = 26
    i2 = 36
    # seqgl = list(glcnpar(seq1[i1:i2]))
    # seqgl = list(map(glcnweb, seq1[i1:i2]))
