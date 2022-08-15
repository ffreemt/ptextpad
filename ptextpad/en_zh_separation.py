# encoding: utf-8
"""
_enzhmap, adjust_zero
en_zh_separation ==> fmax, bmax, fmin, bmin
"""
import re


def _enzhmap(x_char):
    """
    map x to 1 if ascii; -1 if Chinese, 0 if numerical; '' otherwise
    >>> _enzhmap('x')
    1
    >>> _enzhmap('中')
    -1
    >>> _enzhmap('3')
    0
    >>> _enzhmap('xy')

    >>> _enzhmap(' ')
    ''
    """
    enmatch = re.compile("([a-zA-Z]?)")
    zhmatch = re.compile("([……一-﨩、，。！：？“”——‘（）；’《》□•]?)")
    dmatch = re.compile(r"([\d]?)")

    if len(x_char) != 1:
        return None
    # en==>1
    # zh ==> #-2
    if enmatch.match(x_char).groups()[0]:
        return 1
    if zhmatch.match(x_char).groups()[0]:
        return -1
    if dmatch.match(x_char).groups()[0]:
        return 0
    return ""


def adjust_zero(list01e):
    """
    list01e: list of 0,1,-1,empty
    adjudt 0 to be the same as the following 1 or -1
    >>> list01e = [0, '', 1, 1,  '', '', '', '', 1, 1, '', 1, 1, 1, '', 0, '', -1, -1, -1, '', -1]
    >>> adjust_zero(list01e)
    [1, '', 1, 1, '', '', '', '', 1, 1, '', 1, 1, 1, '', -1, '', -1, -1, -1, '', -1]
    >>> list01e = [0, '', 1, 1, '', '', '', 1, 1, 1, 1, 0]
    >>> adjust_zero(list01e)
    [1, '', 1, 1, '', '', '', 1, 1, 1, 1, 1]
    >>> list01e = [0, '', 1, 1, 1, 1, '', '', '', 1, 1, 1, -1, 0]
    >>> adjust_zero(list01e)
    [1, '', 1, 1, 1, 1, '', '', '', 1, 1, 1, -1, -1]
    """
    temp = list01e
    pos0 = list()
    len0 = len(temp)
    for i in range(len0):
        if temp[len0 - 1 - i] == 0:
            pos0 += [len0 - 1 - i]
    for tempi0 in pos0:
        tempi1 = tempi0
        while (temp[tempi1] == "" or (temp[tempi1] == 0)) and tempi1 < (len0 - 1):
            tempi1 += 1

        temp[tempi0] = temp[tempi1]

    tempi1 = len0 - 1
    if temp[len0 - 1] == 0:
        while tempi1 > 1:
            tempi1 -= 1
            if temp[tempi1] == 1 or temp[tempi1] == -1:
                temp[len0 - 1] = temp[tempi1]
                break
        else:
            temp[len0 - 1] = temp[0]
    return temp


def en_zh_separation(para):
    """para: str or unicode
    >>> para = '1 ashl,  sadlkj lj asd 1 是大红.。'

    # >>> en_zh_separation(para)
    # '1 ashl,  sadlkj lj asd ','1 是大红.。'
    # >>> para = para + para
    """
    import logging

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())
    # if isinstance(para, basestring):
    if not isinstance(para, str):
        logger.warning("Input not a string, exiting...")
        return None

    # convverts to numbers
    # ppp000dd00ppp0000dddmmmm
    # pdm==> pmm
    # mmmmdppp:  mdp==> mpp

    seq01 = list(map(_enzhmap, para))
    temp = adjust_zero(seq01)
    len0 = len(temp)
    sum_f = 0
    sum_f_list = list()
    sum_b = 0
    sum_b_list = list()
    for i000 in range(len0):
        if temp[i000] != "":
            sum_f += temp[i000]
        sum_f_list += [sum_f]
    for i000 in range(len0):
        if temp[len0 - 1 - i000] != "":
            sum_b += temp[len0 - 1 - i000]
        sum_b_list += [sum_b]
    # sum_b_list.reverse()

    fmax = sum_f_list.index(max(sum_f_list))
    bmin = len0 - 1 - sum_b_list.index(min(sum_b_list))

    fmin = sum_f_list.index(min(sum_f_list))
    bmax = len0 - 1 - sum_b_list.index(max(sum_b_list))

    # print(fmax, bmin, fmin, bmax)
    # return fmax, bmin, fmin, bmax
    # return fmax, bmax, fmin, bmin
    if bmin - fmax < len0 and bmin - fmax > 0:
        breakpoint0 = bmin
    if bmax - fmin < len0 and bmax - fmin > 0:
        breakpoint1 = bmax

    if "breakpoint0" in locals() and "breakpoint1" in locals():
        if breakpoint1 > breakpoint0:
            breakpoint = breakpoint1
        else:
            breakpoint = breakpoint0
    else:
        if "breakpoint0" in locals():
            breakpoint = breakpoint0
        if "breakpoint1" in locals():
            breakpoint = breakpoint1

    if fmax == bmin and fmin == bmax:
        breakpoint = 1 + max(fmax, bmin, fmin, bmax)

    if "breakpoint" not in locals():
        logger.error("bp not defined")
        return 0

    # print(breakpoint)
    if breakpoint < 2:
        breakpoint = 0
    if len0 - breakpoint < 2:
        breakpoint = len0

    return breakpoint


def _test():
    import doctest

    doctest.testmod()


if __name__ == "__main__":
    _test()
# in ipython: exec(open(r"").read())
