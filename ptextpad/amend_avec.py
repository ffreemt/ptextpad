import logging

from .para_gc import align_blocks_modi

# from para_gc import check_avec


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# import pytest

# logger.level=10
# logger.info(" __name__={} ".format(__name__))

# s1 = [39]
# s2 = [57,17,39]

# avec = align_blocks_modi(s1,s2)
# avec = align_blocks_modi(s2,s1)

# cvec = check_avec(avec, len(s1)-1,len(s2)-1 )
# cvec = check_avec(avec, len(s2)-1,len(s1)-1 )


def amend_avec(avec, cvec):
    """
    avec0 = amendavec(avec,cvec)
    avec = alignblocksmodi(s1,s2)
    cvec = check_avec(avec)
    """

    tmpavec = avec[:]

    avec0 = [el[0] for el in avec]
    avec1 = [el[1] for el in avec]

    if not avec0:  # empty avec0
        logger.debug(" avec0 is empty, return empty. ")
        logger.debug("avec: %s, cvec: %s", avec, cvec)
        return avec

    if not avec1:  # empty avec0
        logger.debug(" avec1 is empty, return empty. ")
        logger.debug(" %s ", avec)
        return avec

    max0 = max(avec0)
    max1 = max(avec1)

    for el in cvec[0]:
        # logger.debug("tmpavec={} el={} ".format(tmpavec,el))

        flag = False
        if el == 0:
            i = el
            while not flag and i <= max0:
                i += 1
                try:
                    i0 = avec0.index(i)
                    flag = True
                except Exception:
                    flag = False
            if not flag:
                logger.warning(" Cant locate pos, exiting... ")
            else:  # insert a pair closest to pos 0
                avec0.insert(i0, el)
                avec1.insert(i0, tmpavec[i0][1])
                tmpavec.insert(i0, (el, tmpavec[i0][1]))
        else:
            i = el
            while not flag and i >= 0:
                i -= 1
                avec0r = avec0[:]
                avec0r.reverse()
                len0 = len(avec0)

                try:
                    i0 = avec0r.index(i)
                    flag = True
                except Exception:
                    flag = False
                # logger.debug(" i={} flag={} ".format(i,flag))

            if not flag:
                logger.warning(" Cant locate pos, exiting.... ")
            else:  # insert a pair
                avec0.insert(len0 - i0, el)
                avec1.insert(len0 - i0, tmpavec[len0 - 1 - i0][1])
                tmpavec.insert(len0 - i0, (el, tmpavec[len0 - 1 - i0][1]))

        # logger.debug(" tmpavec={} avec0={} avec1={}".format(tmpavec,avec0,avec1))

    logger.debug(">>> cvec1={} ".format(cvec[1]))
    for el in cvec[1]:
        # logger.debug(" tmpavec={} el={}".format(tmpavec,el))
        flag = False
        if el == 0:
            i = el
            while not flag and i <= max1:
                i += 1
                try:
                    i0 = avec1.index(i)
                    flag = True
                except Exception:
                    flag = False
            if not flag:
                logger.warning(" Cant locate pos, exiting... ")
            else:  # insert a pair closest to pos 0
                avec0.insert(i0, tmpavec[i0][0])
                avec1.insert(i0, el)
                tmpavec.insert(i0, (tmpavec[i0][0], el))

        else:
            i = el
            while not flag and i >= 0:
                i -= 1
                avec1r = avec1[:]
                avec1r.reverse()
                len1 = len(avec1)
                try:
                    i0 = avec1r.index(i)
                    flag = True
                except Exception:
                    flag = False
            if not flag:
                logger.warning(" Cant locate pos, exiting.... ")
            else:  # insert a pair
                avec0.insert(len1 - i0, tmpavec[len1 - 1 - i0][0])
                avec1.insert(len1 - i0, el)
                tmpavec.insert(len1 - i0, (tmpavec[len1 - 1 - i0][0], el))

        # logger.debug(" tmpavec={} avec0={} avec1={}".format(tmpavec,avec0,avec1))

    return tmpavec


def test_1():
    s1 = [
        38,
        20,
        33,
        107,
        35,
        33,
        35,
        33,
        13,
        160,
        97,
        36,
        41,
        85,
        71,
        72,
        65,
        20,
        43,
        33,
        28,
        38,
        52,
        62,
        38,
        35,
        51,
        55,
        97,
        42,
    ]
    s2 = [2, 20, 30, 16, 5, 31, 20]
    avec = align_blocks_modi(s1, s2)

    # assert 1==1
    # assert 1==2
    assert avec == [
        (0, 0),
        (1, 0),
        (3, 1),
        (4, 1),
        (9, 2),
        (10, 2),
        (13, 3),
        (14, 3),
        (15, 4),
        (16, 4),
        (22, 5),
        (23, 5),
        (27, 6),
        (28, 6),
    ]


if __name__ == "__main__":
    pass
    # import doctest
    # doctest.testmod()
